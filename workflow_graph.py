"""
LangGraph를 사용한 멀티 에이전트 워크플로우 구현
Agent 1(기획) → Agent 2(작성) 간 데이터 흐름을 관리합니다.
"""
from typing import Literal
from langgraph.graph import StateGraph, END
from workflow_state import WorkflowState
from agent_planner import planner_node
from agent_writer import writer_node


def create_workflow() -> StateGraph:
    """
    멀티 에이전트 워크플로우 그래프를 생성합니다.

    워크플로우 흐름:
    1. START → planner (Agent 1: Gemini)
    2. planner → topic_selection (사용자 선택 대기)
    3. topic_selection → writer (Agent 2: Claude)
    4. writer → END
    """

    # StateGraph 초기화
    workflow = StateGraph(WorkflowState)

    # 노드 추가
    workflow.add_node("planner", planner_node)
    workflow.add_node("writer", writer_node)
    workflow.add_node("topic_selection", topic_selection_node)

    # 엣지 정의
    workflow.set_entry_point("planner")
    workflow.add_edge("planner", "topic_selection")
    workflow.add_edge("topic_selection", "writer")
    workflow.add_edge("writer", END)

    return workflow


def topic_selection_node(state: WorkflowState) -> WorkflowState:
    """
    사용자가 주제를 선택할 수 있도록 대기하는 노드
    실제 구현에서는 사용자 입력을 받아야 하지만,
    여기서는 첫 번째 주제를 자동 선택합니다.
    """
    if state.get("topic_suggestions") and not state.get("selected_topic"):
        # 첫 번째 주제 자동 선택 (데모용)
        state["selected_topic"] = state["topic_suggestions"][0]

    return state


def create_advanced_workflow() -> StateGraph:
    """
    고급 워크플로우: Agent 3(편집), Agent 4(이미지), Agent 5(퍼블리싱) 포함
    추후 확장을 위한 스켈레톤 코드
    """

    workflow = StateGraph(WorkflowState)

    # 기본 노드
    workflow.add_node("planner", planner_node)
    workflow.add_node("topic_selection", topic_selection_node)
    workflow.add_node("writer", writer_node)

    # 추가 노드 (스켈레톤)
    # workflow.add_node("reviewer", reviewer_node)  # Agent 3
    # workflow.add_node("image_generator", image_generator_node)  # Agent 4
    # workflow.add_node("publisher", publisher_node)  # Agent 5

    # 기본 플로우
    workflow.set_entry_point("planner")
    workflow.add_edge("planner", "topic_selection")
    workflow.add_edge("topic_selection", "writer")

    # 조건부 라우팅 (추후 구현)
    # workflow.add_conditional_edges(
    #     "reviewer",
    #     should_retry,
    #     {
    #         "retry": "writer",  # 검수 실패 시 다시 작성
    #         "continue": "image_generator"  # 검수 통과 시 이미지 생성
    #     }
    # )

    workflow.add_edge("writer", END)

    return workflow


def should_retry(state: WorkflowState) -> Literal["retry", "continue"]:
    """
    Agent 3(검수) 결과에 따라 다음 노드를 결정합니다.
    - retry: Agent 2로 돌아가서 다시 작성
    - continue: Agent 4(이미지 생성)로 진행
    """
    if state.get("retry_count", 0) >= 2:
        # 최대 재시도 횟수 초과 시 강제 진행
        return "continue"

    if not state.get("review_passed", False):
        state["retry_count"] = state.get("retry_count", 0) + 1
        return "retry"

    return "continue"
