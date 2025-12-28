"""
Agent 1: 기획자 에이전트 (Gemini)
업종을 분석하고 인기 주제와 키워드를 추천합니다.
"""
import os
from typing import List
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import SystemMessage, HumanMessage
from workflow_state import WorkflowState, TopicSuggestion


class PlannerAgent:
    """Gemini 기반 주제 기획 에이전트"""

    def __init__(self, model_name: str = "gemini-1.5-pro"):
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            raise ValueError("GOOGLE_API_KEY가 설정되지 않았습니다.")

        self.llm = ChatGoogleGenerativeAI(
            model=model_name,
            google_api_key=api_key,
            temperature=0.7
        )

    def suggest_topics(self, state: WorkflowState) -> WorkflowState:
        """
        업종을 분석하여 블로그 주제를 추천합니다.

        Args:
            state: 현재 워크플로우 상태 (business_type 필요)

        Returns:
            업데이트된 상태 (topic_suggestions 추가)
        """
        business_type = state["business_type"]

        system_prompt = """당신은 한국의 블로그 마케팅 전문가입니다.
사용자의 업종을 분석하여 SEO에 유리하고 실제 고객이 많이 검색하는 주제를 추천해야 합니다.

다음 기준으로 주제를 선정하세요:
1. 높은 검색 볼륨을 가진 키워드
2. 실용적이고 즉시 적용 가능한 정보
3. 계절성 또는 최신 트렌드 반영
4. 전문성을 드러낼 수 있는 주제

반드시 JSON 형식으로 응답하세요:
{
  "suggestions": [
    {
      "keyword": "핵심 키워드",
      "title": "블로그 제목 (35자 이내)",
      "reason": "이 주제를 추천하는 이유"
    }
  ]
}
"""

        user_prompt = f"""업종: {business_type}

위 업종에 적합한 블로그 주제를 5개 추천해주세요.
각 주제는 실제로 고객이 검색할 만한 키워드를 포함해야 합니다."""

        messages = [
            SystemMessage(content=system_prompt),
            HumanMessage(content=user_prompt)
        ]

        response = self.llm.invoke(messages)

        # 응답 파싱 (간단한 구현)
        topics = self._parse_response(response.content, business_type)

        # 상태 업데이트
        state["topic_suggestions"] = topics
        state["current_step"] = "topic_selection"

        return state

    def _parse_response(self, response: str, business_type: str) -> List[TopicSuggestion]:
        """LLM 응답을 파싱하여 TopicSuggestion 리스트로 변환"""
        import json
        import re

        # JSON 블록 추출
        json_match = re.search(r'\{[\s\S]*\}', response)
        if json_match:
            try:
                data = json.loads(json_match.group())
                suggestions = data.get("suggestions", [])
                return [
                    TopicSuggestion(
                        keyword=s.get("keyword", ""),
                        title=s.get("title", ""),
                        reason=s.get("reason", "")
                    )
                    for s in suggestions
                ]
            except json.JSONDecodeError:
                pass

        # 파싱 실패 시 기본값 반환
        return [
            TopicSuggestion(
                keyword=f"{business_type} 팁",
                title=f"{business_type}가 알려주는 필수 정보",
                reason="기본 추천 주제입니다."
            )
        ]


def planner_node(state: WorkflowState) -> WorkflowState:
    """LangGraph 노드로 사용할 함수"""
    agent = PlannerAgent()
    return agent.suggest_topics(state)
