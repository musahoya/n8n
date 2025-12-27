"""
Agent 4: 이미지 프롬프트 생성 에이전트
Gemini로 블로그 이미지에 적합한 프롬프트를 생성합니다.
(사용자가 직접 이미지를 업로드하므로 생성은 하지 않음)
"""
from multi_model_agent import MultiModelAgent


class ImagePromptAgent:
    """이미지 프롬프트 생성 에이전트 (Gemini 고정)"""

    def __init__(self, gemini_api_key: str):
        """
        Args:
            gemini_api_key: Google Gemini API 키
        """
        self.agent = MultiModelAgent(
            model_type="gemini",
            gemini_api_key=gemini_api_key,
            temperature=0.9  # 창의적인 프롬프트 생성
        )

    def generate_image_prompt(
        self,
        content: str,
        keyword: str,
        platform: str
    ) -> str:
        """
        콘텐츠를 분석하여 적합한 이미지 프롬프트를 생성합니다.

        Args:
            content: 블로그 콘텐츠
            keyword: 주제 키워드
            platform: 플랫폼

        Returns:
            이미지 생성용 프롬프트 (영문)
        """
        system_prompt = """당신은 블로그 썸네일 이미지 전문가입니다.
블로그 콘텐츠를 분석하여 DALL-E나 Midjourney에서 사용할 수 있는
고품질 이미지 프롬프트를 생성해야 합니다.

【프롬프트 작성 원칙】
1. 영문으로 작성
2. 구체적이고 상세한 묘사
3. 스타일 지정 (modern, minimalist, professional 등)
4. 색감 및 분위기 명시
5. 한국적 요소 포함 (필요시)

【좋은 예시】
"A professional Korean accountant working on tax documents,
clean modern office setting, soft natural lighting,
minimalist design with pastel blue and white colors,
high quality illustration style, organized desk with calculator"

【나쁜 예시】
"tax" (너무 단순함)
"세무사 사무실" (한글 사용)

완성된 프롬프트만 작성하세요. 부가 설명은 하지 마세요."""

        user_prompt = f"""다음 블로그 글에 어울리는 썸네일 이미지 프롬프트를 생성해주세요.

【키워드】 {keyword}
【플랫폼】 {platform}

【콘텐츠 요약】
{content[:500]}...

위 내용을 바탕으로 영문 이미지 프롬프트를 작성해주세요."""

        response = self.agent.invoke(system_prompt, user_prompt)
        # 따옴표 제거 및 정리
        return response.strip().strip('"').strip("'")
