"""
Agent 2: 작가 에이전트 (Claude)
선택된 주제로 플랫폼별 맞춤 콘텐츠를 작성합니다.
"""
import os
from typing import List
from langchain_anthropic import ChatAnthropic
from langchain_core.messages import SystemMessage, HumanMessage
from workflow_state import WorkflowState, ContentVersion


class WriterAgent:
    """Claude 기반 콘텐츠 작성 에이전트"""

    def __init__(self, model_name: str = "claude-3-5-sonnet-20241022"):
        api_key = os.getenv("ANTHROPIC_API_KEY")
        if not api_key:
            raise ValueError("ANTHROPIC_API_KEY가 설정되지 않았습니다.")

        self.llm = ChatAnthropic(
            model=model_name,
            anthropic_api_key=api_key,
            temperature=0.8,
            max_tokens=4096
        )

    def write_content(self, state: WorkflowState) -> WorkflowState:
        """
        선택된 주제로 플랫폼별 콘텐츠를 작성합니다.

        Args:
            state: 현재 워크플로우 상태 (selected_topic 필요)

        Returns:
            업데이트된 상태 (content_versions 추가)
        """
        if not state.get("selected_topic"):
            raise ValueError("선택된 주제가 없습니다.")

        topic = state["selected_topic"]
        business_type = state["business_type"]

        # 플랫폼별로 콘텐츠 생성
        content_versions = []

        # 1. 네이버 블로그용 (친근하고 이모지 활용)
        naver_content = self._generate_platform_content(
            topic, business_type, "naver"
        )
        content_versions.append(ContentVersion(
            platform="naver",
            content=naver_content,
            tone="friendly"
        ))

        # 2. 티스토리용 (정보 전달 중심, 깔끔한 구조)
        tistory_content = self._generate_platform_content(
            topic, business_type, "tistory"
        )
        content_versions.append(ContentVersion(
            platform="tistory",
            content=tistory_content,
            tone="professional"
        ))

        # 3. 구글 블로그용 (SEO 최적화, 전문적)
        google_content = self._generate_platform_content(
            topic, business_type, "google"
        )
        content_versions.append(ContentVersion(
            platform="google",
            content=google_content,
            tone="professional"
        ))

        # 상태 업데이트
        state["content_versions"] = content_versions
        state["current_step"] = "content_review"

        return state

    def _generate_platform_content(
        self, topic, business_type: str, platform: str
    ) -> str:
        """플랫폼별 맞춤 콘텐츠 생성"""

        platform_guidelines = {
            "naver": {
                "tone": "친근하고 대화하듯이",
                "structure": "짧은 문단, 이모지 활용, 공감 유도",
                "style": "카카오톡 대화하듯 편안하게",
                "example": "안녕하세요! 😊 오늘은 여러분께..."
            },
            "tistory": {
                "tone": "정보 전달 중심, 신뢰감 있게",
                "structure": "명확한 소제목, 리스트 활용, 단계별 설명",
                "style": "전문가가 설명하는 느낌",
                "example": "## 1. 핵심 정보\n\n본문 내용..."
            },
            "google": {
                "tone": "전문적이고 객관적",
                "structure": "SEO 키워드 자연스럽게 배치, H2/H3 태그 활용",
                "style": "검색 엔진 최적화",
                "example": "# 제목 (H1)\n\n## 주요 내용 (H2)..."
            }
        }

        guideline = platform_guidelines[platform]

        system_prompt = f"""당신은 한국의 전문 블로그 작가입니다.
주어진 주제로 {platform} 플랫폼에 최적화된 블로그 글을 작성해야 합니다.

【플랫폼별 가이드라인】
- 톤: {guideline['tone']}
- 구조: {guideline['structure']}
- 스타일: {guideline['style']}

【작성 원칙】
1. 독자가 실제로 적용할 수 있는 구체적인 정보 제공
2. 전문성과 신뢰감을 주는 내용
3. 적절한 길이 (1,200~1,800자)
4. 자연스러운 키워드 배치
5. 행동 유도 (CTA) 포함

【금지 사항】
- 과도한 광고성 문구
- 검증되지 않은 정보
- 비속어나 부적절한 표현
"""

        user_prompt = f"""다음 주제로 {platform} 블로그 글을 작성해주세요.

【업종】 {business_type}
【키워드】 {topic.keyword}
【제목】 {topic.title}
【이유】 {topic.reason}

위 정보를 바탕으로 완성도 높은 블로그 글을 작성해주세요.
반드시 한국어로 작성하고, {platform}의 특성에 맞게 작성하세요."""

        messages = [
            SystemMessage(content=system_prompt),
            HumanMessage(content=user_prompt)
        ]

        response = self.llm.invoke(messages)
        return response.content


def writer_node(state: WorkflowState) -> WorkflowState:
    """LangGraph 노드로 사용할 함수"""
    agent = WriterAgent()
    return agent.write_content(state)
