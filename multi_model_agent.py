"""
멀티 모델 지원 에이전트
사용자가 선택한 AI 모델(Gemini/Claude/GPT)로 동적으로 작업을 수행합니다.
"""
from typing import Literal, Optional
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_anthropic import ChatAnthropic
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage
from langchain_core.language_models.chat_models import BaseChatModel


ModelType = Literal["gemini", "claude", "gpt"]


class MultiModelAgent:
    """여러 AI 모델을 지원하는 범용 에이전트"""

    def __init__(
        self,
        model_type: ModelType,
        gemini_api_key: Optional[str] = None,
        claude_api_key: Optional[str] = None,
        openai_api_key: Optional[str] = None,
        temperature: float = 0.7
    ):
        """
        Args:
            model_type: 사용할 모델 ("gemini", "claude", "gpt")
            gemini_api_key: Google Gemini API 키
            claude_api_key: Anthropic Claude API 키
            openai_api_key: OpenAI GPT API 키
            temperature: 생성 온도
        """
        self.model_type = model_type
        self.temperature = temperature
        self.llm = self._create_llm(
            model_type, gemini_api_key, claude_api_key, openai_api_key
        )

    def _create_llm(
        self,
        model_type: ModelType,
        gemini_api_key: Optional[str],
        claude_api_key: Optional[str],
        openai_api_key: Optional[str]
    ) -> BaseChatModel:
        """선택된 모델에 따라 LLM 인스턴스 생성"""

        if model_type == "gemini":
            if not gemini_api_key:
                raise ValueError("Gemini API 키가 필요합니다.")
            return ChatGoogleGenerativeAI(
                model="gemini-2.5-flash",
                google_api_key=gemini_api_key,
                temperature=self.temperature,
                convert_system_message_to_human=True  # Gemini는 시스템 메시지를 지원하지 않으므로 변환
            )

        elif model_type == "claude":
            if not claude_api_key:
                raise ValueError("Claude API 키가 필요합니다.")
            return ChatAnthropic(
                model="claude-3-5-sonnet-20241022",  # Claude 3.5 Sonnet (2024년 10월)
                api_key=claude_api_key,  # anthropic_api_key 대신 api_key 사용
                temperature=self.temperature,
                max_tokens=8192  # Claude 3.5는 8192 토큰 지원
            )

        elif model_type == "gpt":
            if not openai_api_key:
                raise ValueError("OpenAI API 키가 필요합니다.")
            return ChatOpenAI(
                model="gpt-4o",
                openai_api_key=openai_api_key,
                temperature=self.temperature
            )

        else:
            raise ValueError(f"지원하지 않는 모델: {model_type}")

    def invoke(self, system_prompt: str, user_prompt: str) -> str:
        """
        프롬프트를 실행하고 결과를 반환합니다.

        Args:
            system_prompt: 시스템 프롬프트
            user_prompt: 사용자 프롬프트

        Returns:
            AI 모델의 응답
        """
        try:
            messages = [
                SystemMessage(content=system_prompt),
                HumanMessage(content=user_prompt)
            ]

            response = self.llm.invoke(messages)
            return response.content
        except Exception as e:
            # 에러 발생 시 상세한 정보 제공
            error_msg = f"{self.get_model_name()} API 오류: {str(e)}"
            print(f"[ERROR] {error_msg}")
            raise Exception(error_msg)

    def get_model_name(self) -> str:
        """현재 사용 중인 모델 이름 반환"""
        model_names = {
            "gemini": "Gemini 2.5 Flash",
            "claude": "Claude 3.5 Sonnet",
            "gpt": "GPT-4o"
        }
        return model_names[self.model_type]
