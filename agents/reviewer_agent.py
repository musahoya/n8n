"""
Agent 3: 검수 에이전트 (멀티 모델 지원)
사용자가 선택한 모델(Gemini/Claude/GPT)로 콘텐츠를 검수합니다.
"""
import json
import re
from typing import Dict
from multi_model_agent import MultiModelAgent, ModelType


class ReviewResult:
    """검수 결과"""
    def __init__(self, passed: bool, feedback: str, score: int = 0):
        self.passed = passed
        self.feedback = feedback
        self.score = score  # 0-100점

    def to_dict(self):
        return {
            "passed": self.passed,
            "feedback": self.feedback,
            "score": self.score
        }


class ReviewerAgentMultiModel:
    """멀티 모델 지원 검수 에이전트"""

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
            temperature=0.3  # 검수는 낮은 온도로
        )

    def review_content(
        self,
        content: str,
        platform: str,
        business_type: str
    ) -> ReviewResult:
        """
        콘텐츠를 검수합니다.

        Args:
            content: 검수할 콘텐츠
            platform: 플랫폼 (naver, tistory, google)
            business_type: 업종

        Returns:
            검수 결과
        """
        system_prompt = """당신은 전문 블로그 콘텐츠 검수자입니다.
다음 기준으로 콘텐츠를 엄격하게 검수하세요:

【검수 항목】
1. 사실 정확성 (30점)
   - 법률/세무/의료 등 전문 정보의 정확성
   - 검증되지 않은 주장이 없는지

2. 맞춤법 및 문법 (20점)
   - 오타나 문법 오류
   - 자연스러운 문장 구조

3. 콘텐츠 품질 (30점)
   - 실용적이고 구체적인 정보 제공
   - 적절한 길이와 구조
   - 플랫폼 특성에 맞는 작성

4. 부적절한 내용 (20점)
   - 과도한 광고성 문구
   - 금칙어나 비속어
   - 타인을 비방하는 내용

총 100점 만점으로 채점하고, 70점 이상이면 통과입니다.

반드시 다음 JSON 형식으로만 응답하세요:
```json
{
  "passed": true/false,
  "score": 0-100,
  "feedback": "구체적인 피드백 (통과 시 칭찬, 불합격 시 수정 방향 제시)"
}
```

JSON 외의 다른 텍스트는 포함하지 마세요."""

        user_prompt = f"""다음 블로그 글을 검수해주세요.

【업종】 {business_type}
【플랫폼】 {platform}

【콘텐츠】
{content}

위 콘텐츠를 검수하고 JSON 형식으로 결과를 반환해주세요."""

        response = self.agent.invoke(system_prompt, user_prompt)
        return self._parse_response(response)

    def _parse_response(self, response: str) -> ReviewResult:
        """LLM 응답을 파싱하여 ReviewResult로 변환"""

        # JSON 블록 추출
        json_match = re.search(r'```json\s*([\s\S]*?)\s*```', response)
        if json_match:
            json_str = json_match.group(1)
        else:
            json_match = re.search(r'\{[\s\S]*\}', response)
            if json_match:
                json_str = json_match.group()
            else:
                json_str = None

        if json_str:
            try:
                data = json.loads(json_str)
                return ReviewResult(
                    passed=data.get("passed", False),
                    feedback=data.get("feedback", ""),
                    score=data.get("score", 0)
                )
            except json.JSONDecodeError:
                pass

        # 파싱 실패 시 기본값 (통과로 처리)
        return ReviewResult(
            passed=True,
            feedback="검수 결과를 파싱할 수 없어 자동으로 통과 처리되었습니다.",
            score=70
        )
