"""
Agent 1: 주제 기획 에이전트 (멀티 모델 지원)
사용자가 선택한 모델(Gemini/Claude/GPT)로 주제를 추천합니다.
"""
import json
import re
from typing import List
from multi_model_agent import MultiModelAgent, ModelType


class TopicSuggestion:
    """주제 제안 데이터 모델"""
    def __init__(self, keyword: str, title: str, reason: str):
        self.keyword = keyword
        self.title = title
        self.reason = reason

    def to_dict(self):
        return {
            "keyword": self.keyword,
            "title": self.title,
            "reason": self.reason
        }


class PlannerAgentMultiModel:
    """멀티 모델 지원 주제 기획 에이전트"""

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
            temperature=0.7
        )

    def suggest_topics(self, business_type: str) -> List[TopicSuggestion]:
        """
        업종을 분석하여 블로그 주제를 추천합니다.

        Args:
            business_type: 업종 (예: "세무사", "변호사", "카페")

        Returns:
            추천된 주제 목록
        """
        system_prompt = """당신은 한국의 블로그 마케팅 전문가입니다.
사용자의 업종을 분석하여 SEO에 유리하고 실제 고객이 많이 검색하는 주제를 추천해야 합니다.

다음 기준으로 주제를 선정하세요:
1. 높은 검색 볼륨을 가진 키워드
2. 실용적이고 즉시 적용 가능한 정보
3. 계절성 또는 최신 트렌드 반영
4. 전문성을 드러낼 수 있는 주제

반드시 다음 JSON 형식으로만 응답하세요:
```json
{
  "suggestions": [
    {
      "keyword": "핵심 키워드",
      "title": "블로그 제목 (35자 이내)",
      "reason": "이 주제를 추천하는 이유"
    }
  ]
}
```

JSON 외의 다른 텍스트는 포함하지 마세요."""

        user_prompt = f"""업종: {business_type}

위 업종에 적합한 블로그 주제를 5개 추천해주세요.
각 주제는 실제로 고객이 검색할 만한 키워드를 포함해야 합니다."""

        response = self.agent.invoke(system_prompt, user_prompt)
        return self._parse_response(response, business_type)

    def _parse_response(self, response: str, business_type: str) -> List[TopicSuggestion]:
        """LLM 응답을 파싱하여 TopicSuggestion 리스트로 변환"""

        # JSON 블록 추출 (```json ... ``` 형식 처리)
        json_match = re.search(r'```json\s*([\s\S]*?)\s*```', response)
        if json_match:
            json_str = json_match.group(1)
        else:
            # 단순 JSON 객체 추출
            json_match = re.search(r'\{[\s\S]*\}', response)
            if json_match:
                json_str = json_match.group()
            else:
                json_str = None

        if json_str:
            try:
                data = json.loads(json_str)
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
