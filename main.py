"""
멀티 에이전트 워크플로우 메인 실행 스크립트
Agent 1 (Gemini 기획) → Agent 2 (Claude 작성) 데모
"""
import os
from dotenv import load_dotenv
from workflow_graph import create_workflow
from workflow_state import WorkflowState


def print_separator():
    """구분선 출력"""
    print("\n" + "=" * 80 + "\n")


def display_topics(state: WorkflowState):
    """추천된 주제 목록 출력"""
    print("🎯 추천 주제 목록:")
    print_separator()

    topics = state.get("topic_suggestions", [])
    for i, topic in enumerate(topics, 1):
        print(f"{i}. 키워드: {topic.keyword}")
        print(f"   제목: {topic.title}")
        print(f"   이유: {topic.reason}")
        print()


def display_content(state: WorkflowState):
    """생성된 콘텐츠 출력"""
    print("📝 생성된 콘텐츠:")
    print_separator()

    contents = state.get("content_versions", [])
    for content in contents:
        print(f"【{content.platform.upper()} 버전】")
        print(f"톤: {content.tone}")
        print(f"\n{content.content[:500]}...")  # 처음 500자만 출력
        print_separator()


def run_workflow(business_type: str):
    """
    워크플로우를 실행합니다.

    Args:
        business_type: 사용자의 업종 (예: "세무사", "변호사", "카페")
    """

    # 환경 변수 로드
    load_dotenv()

    # API 키 확인
    required_keys = ["GOOGLE_API_KEY", "ANTHROPIC_API_KEY"]
    missing_keys = [key for key in required_keys if not os.getenv(key)]

    if missing_keys:
        print(f"❌ 다음 API 키가 설정되지 않았습니다: {', '.join(missing_keys)}")
        print("📝 .env 파일을 생성하고 API 키를 설정해주세요.")
        print("   예시: .env.example 파일을 참고하세요.")
        return

    print("🚀 멀티 에이전트 워크플로우 시작")
    print(f"📌 업종: {business_type}")
    print_separator()

    # 초기 상태 설정
    initial_state: WorkflowState = {
        "business_type": business_type,
        "topic_suggestions": None,
        "selected_topic": None,
        "content_versions": None,
        "review_passed": None,
        "review_feedback": None,
        "image_prompt": None,
        "image_url": None,
        "published_urls": None,
        "retry_count": 0,
        "current_step": "planning"
    }

    # 워크플로우 생성 및 컴파일
    workflow = create_workflow()
    app = workflow.compile()

    try:
        # Step 1: Agent 1 (Gemini) - 주제 기획
        print("🤖 Agent 1 (Gemini) - 주제 기획 중...")
        result = app.invoke(initial_state)

        # 결과 출력
        display_topics(result)

        # Step 2: Agent 2 (Claude) - 콘텐츠 작성
        print("🤖 Agent 2 (Claude) - 콘텐츠 작성 중...")
        print("   (선택된 주제로 자동 진행됩니다)")

        # 콘텐츠 출력
        display_content(result)

        print("✅ 워크플로우 완료!")
        print("\n💡 다음 단계 예정:")
        print("   - Agent 3: GPT-4o로 팩트 체크 및 검수")
        print("   - Agent 4: DALL-E 3로 이미지 생성")
        print("   - Agent 5: 네이버/티스토리 자동 퍼블리싱")

    except Exception as e:
        print(f"❌ 오류 발생: {str(e)}")
        import traceback
        traceback.print_exc()


def interactive_mode():
    """대화형 모드로 실행"""
    print("🎨 멀티 에이전트 블로그 자동화 시스템")
    print_separator()

    business_type = input("📝 업종을 입력하세요 (예: 세무사, 변호사, 카페): ").strip()

    if not business_type:
        print("❌ 업종을 입력해주세요.")
        return

    run_workflow(business_type)


if __name__ == "__main__":
    # 대화형 모드 실행
    interactive_mode()

    # 또는 직접 실행:
    # run_workflow("세무사")
