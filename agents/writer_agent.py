"""
Agent 2: 콘텐츠 작성 에이전트 (멀티 모델 지원)
사용자가 선택한 모델(Gemini/Claude/GPT)로 플랫폼별 콘텐츠를 작성합니다.
"""
from typing import List
from multi_model_agent import MultiModelAgent, ModelType


class ContentVersion:
    """플랫폼별 콘텐츠 버전"""
    def __init__(self, platform: str, content: str, tone: str):
        self.platform = platform
        self.content = content
        self.tone = tone

    def to_dict(self):
        return {
            "platform": self.platform,
            "content": self.content,
            "tone": self.tone
        }


class WriterAgentMultiModel:
    """멀티 모델 지원 콘텐츠 작성 에이전트"""

    def __init__(
        self,
        model_type: ModelType,
        gemini_api_key: str = None,
        claude_api_key: str = None,
        openai_api_key: str = None
    ):
        self.agent = MultiModelAgent(
            model_type=model_type,
            gemini_api_key=gemini_api_key,
            claude_api_key=claude_api_key,
            openai_api_key=openai_api_key,
            temperature=0.8
        )

    def write_content(
        self,
        topic_keyword: str,
        topic_title: str,
        topic_reason: str,
        business_type: str
    ) -> List[ContentVersion]:
        """
        선택된 주제로 플랫폼별 콘텐츠를 작성합니다.

        Args:
            topic_keyword: 주제 키워드
            topic_title: 주제 제목
            topic_reason: 추천 이유
            business_type: 업종

        Returns:
            플랫폼별 콘텐츠 목록
        """
        content_versions = []

        # 1. 네이버 블로그용 (친근하고 이모지 활용)
        naver_content = self._generate_platform_content(
            topic_keyword, topic_title, topic_reason, business_type, "naver"
        )
        content_versions.append(ContentVersion(
            platform="naver",
            content=naver_content,
            tone="friendly"
        ))

        # 2. 티스토리용 (정보 전달 중심, 깔끔한 구조)
        tistory_content = self._generate_platform_content(
            topic_keyword, topic_title, topic_reason, business_type, "tistory"
        )
        content_versions.append(ContentVersion(
            platform="tistory",
            content=tistory_content,
            tone="professional"
        ))

        # 3. 구글 블로그용 (SEO 최적화, 전문적)
        google_content = self._generate_platform_content(
            topic_keyword, topic_title, topic_reason, business_type, "google"
        )
        content_versions.append(ContentVersion(
            platform="google",
            content=google_content,
            tone="professional"
        ))

        return content_versions

    def _generate_platform_content(
        self,
        keyword: str,
        title: str,
        reason: str,
        business_type: str,
        platform: str
    ) -> str:
        """플랫폼별 맞춤 콘텐츠 생성"""

        platform_guidelines = {
            "naver": {
                "tone": "친근하고 대화하듯이",
                "structure": "짧은 문단, 이모지 활용, 공감 유도",
                "style": "카카오톡 대화하듯 편안하게",
                "length": "1,200~1,500자"
            },
            "tistory": {
                "tone": "정보 전달 중심, 신뢰감 있게",
                "structure": "명확한 소제목, 리스트 활용, 단계별 설명",
                "style": "전문가가 설명하는 느낌",
                "length": "1,500~2,000자"
            },
            "google": {
                "tone": "전문적이고 객관적",
                "structure": "SEO 키워드 자연스럽게 배치, H2/H3 태그 활용",
                "style": "검색 엔진 최적화",
                "length": "1,800~2,500자"
            }
        }

        guideline = platform_guidelines[platform]

        system_prompt = f"""당신은 한국의 전문 블로그 작가입니다.
주어진 주제로 {platform} 플랫폼에 최적화된 블로그 글을 작성해야 합니다.

【플랫폼별 가이드라인】
- 톤: {guideline['tone']}
- 구조: {guideline['structure']}
- 스타일: {guideline['style']}
- 길이: {guideline['length']}

【작성 원칙】
1. 독자가 실제로 적용할 수 있는 구체적인 정보 제공
2. 전문성과 신뢰감을 주는 내용
3. 자연스러운 키워드 배치
4. 행동 유도 (CTA) 포함

【금지 사항】
- 과도한 광고성 문구
- 검증되지 않은 정보
- 비속어나 부적절한 표현
- 지나치게 짧거나 긴 내용

완성된 블로그 글만 작성하세요. 부가 설명은 하지 마세요."""

        user_prompt = f"""다음 주제로 {platform} 블로그 글을 작성해주세요.

【업종】 {business_type}
【키워드】 {keyword}
【제목】 {title}
【선정 이유】 {reason}

위 정보를 바탕으로 완성도 높은 블로그 글을 작성해주세요.
반드시 한국어로 작성하고, {platform}의 특성에 맞게 작성하세요."""

        response = self.agent.invoke(system_prompt, user_prompt)
        return response
