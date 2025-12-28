"""
간단한 사용 예제

실제 API 키 없이도 시스템 구조를 이해할 수 있도록
모의 데이터를 사용한 예제입니다.
"""
from workflow_state import WorkflowState, TopicSuggestion, ContentVersion


def example_workflow_simulation():
    """
    실제 API 호출 없이 워크플로우 흐름을 시뮬레이션합니다.
    """

    print("=" * 80)
    print("멀티 에이전트 워크플로우 시뮬레이션")
    print("=" * 80)

    # Step 1: 초기 상태
    state: WorkflowState = {
        "business_type": "세무사",
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

    print(f"\n📌 사용자 입력: {state['business_type']}")
    print(f"현재 단계: {state['current_step']}")

    # Step 2: Agent 1 (Gemini) - 주제 기획
    print("\n" + "=" * 80)
    print("🤖 Agent 1 (Gemini) - 주제 기획")
    print("=" * 80)

    state["topic_suggestions"] = [
        TopicSuggestion(
            keyword="종합소득세 절세",
            title="세무사가 알려주는 종합소득세 절세 꿀팁 5가지",
            reason="5월 종합소득세 신고 시즌에 검색량이 급증하는 주제"
        ),
        TopicSuggestion(
            keyword="부가가치세 환급",
            title="부가가치세 환급 받는 방법, 놓치지 마세요",
            reason="사업자들이 자주 검색하는 실용적인 정보"
        ),
        TopicSuggestion(
            keyword="법인세 신고",
            title="법인세 신고 기간과 절차 완벽 가이드",
            reason="법인 사업자 필수 정보로 수요가 높음"
        )
    ]
    state["current_step"] = "topic_selection"

    print("\n추천된 주제 목록:")
    for i, topic in enumerate(state["topic_suggestions"], 1):
        print(f"\n{i}. {topic.title}")
        print(f"   키워드: {topic.keyword}")
        print(f"   이유: {topic.reason}")

    # Step 3: 주제 선택
    print("\n" + "=" * 80)
    print("✅ 주제 선택")
    print("=" * 80)

    state["selected_topic"] = state["topic_suggestions"][0]
    print(f"\n선택된 주제: {state['selected_topic'].title}")

    # Step 4: Agent 2 (Claude) - 콘텐츠 작성
    print("\n" + "=" * 80)
    print("🤖 Agent 2 (Claude) - 콘텐츠 작성")
    print("=" * 80)

    state["content_versions"] = [
        ContentVersion(
            platform="naver",
            content="""안녕하세요! 😊

오늘은 종합소득세 절세 방법을 알려드릴게요.
5월은 종합소득세 신고의 달이죠!

🎯 절세 꿀팁 5가지

1️⃣ 필요 경비 누락 없이 챙기기
영수증 하나하나가 돈입니다! 📝

2️⃣ 공제 항목 최대한 활용
의료비, 교육비 등 놓치지 마세요 💰

3️⃣ 세액 공제 꼼꼼히 확인
기부금, 연금저축 등을 활용하면 절세 가능해요 ✨

4️⃣ 신고 기한 준수
가산세 피하는 게 최고의 절세! ⏰

5️⃣ 전문가 상담 받기
복잡하면 세무사와 상담하세요 👨‍💼

궁금한 점 있으시면 댓글 남겨주세요! 💬""",
            tone="friendly"
        ),
        ContentVersion(
            platform="tistory",
            content="""## 종합소득세 절세 전략

종합소득세는 개인이 1년간 벌어들인 소득에 대해 부과되는 세금입니다.

### 1. 필요 경비의 정확한 산정

사업과 관련된 모든 지출을 필요 경비로 인정받을 수 있습니다.

- 임차료
- 인건비
- 소모품비
- 접대비

### 2. 소득공제 항목 활용

다음과 같은 항목은 소득에서 공제됩니다:

- 국민연금 보험료
- 건강보험료
- 기부금

### 3. 세액공제 극대화

세액공제는 산출된 세액에서 직접 차감되므로 절세 효과가 큽니다.

### 4. 성실신고 확인대상자 지원

매출액이 일정 규모 이상인 경우, 세무사의 확인을 받으면 세액 공제를 받을 수 있습니다.

### 5. 전문가 상담의 중요성

복잡한 세무 문제는 전문가와 상담하는 것이 가장 확실한 방법입니다.""",
            tone="professional"
        )
    ]
    state["current_step"] = "content_review"

    print("\n생성된 콘텐츠:")
    for content in state["content_versions"]:
        print(f"\n{'=' * 80}")
        print(f"【{content.platform.upper()}】 (톤: {content.tone})")
        print(f"{'=' * 80}")
        print(content.content[:300] + "...")

    # Step 5: 결과 요약
    print("\n" + "=" * 80)
    print("✅ 워크플로우 완료")
    print("=" * 80)

    print(f"\n📊 최종 상태:")
    print(f"   - 업종: {state['business_type']}")
    print(f"   - 추천 주제 수: {len(state['topic_suggestions'])}")
    print(f"   - 선택된 주제: {state['selected_topic'].title}")
    print(f"   - 생성된 콘텐츠: {len(state['content_versions'])}개")
    print(f"   - 현재 단계: {state['current_step']}")

    print("\n💡 다음 단계 (추후 구현):")
    print("   - Agent 3: GPT-4o로 팩트 체크")
    print("   - Agent 4: DALL-E로 이미지 생성")
    print("   - Agent 5: 자동 퍼블리싱")


if __name__ == "__main__":
    example_workflow_simulation()
