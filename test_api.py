"""
API 연결 테스트 스크립트
Gemini와 Claude API가 올바르게 작동하는지 확인합니다.
"""
import os
from dotenv import load_dotenv
from multi_model_agent import MultiModelAgent

# 환경 변수 로드
load_dotenv()


def test_gemini():
    """Gemini API 테스트"""
    print("=" * 60)
    print("🔍 Gemini API 테스트 중...")
    print("=" * 60)

    api_key = os.getenv("GOOGLE_API_KEY")

    if not api_key:
        print("❌ GOOGLE_API_KEY가 설정되지 않았습니다.")
        print("   .env 파일에 GOOGLE_API_KEY를 추가해주세요.")
        return False

    try:
        agent = MultiModelAgent(
            model_type="gemini",
            gemini_api_key=api_key,
            temperature=0.7
        )

        response = agent.invoke(
            system_prompt="당신은 도움이 되는 AI 어시스턴트입니다.",
            user_prompt="안녕하세요! 간단히 인사해주세요."
        )

        print("✅ Gemini API 연결 성공!")
        print(f"응답: {response[:100]}...")
        print()
        return True

    except Exception as e:
        print(f"❌ Gemini API 오류: {str(e)}")
        print()
        return False


def test_claude():
    """Claude API 테스트"""
    print("=" * 60)
    print("🔍 Claude API 테스트 중...")
    print("=" * 60)

    api_key = os.getenv("ANTHROPIC_API_KEY")

    if not api_key:
        print("❌ ANTHROPIC_API_KEY가 설정되지 않았습니다.")
        print("   .env 파일에 ANTHROPIC_API_KEY를 추가해주세요.")
        return False

    try:
        agent = MultiModelAgent(
            model_type="claude",
            claude_api_key=api_key,
            temperature=0.7
        )

        response = agent.invoke(
            system_prompt="당신은 도움이 되는 AI 어시스턴트입니다.",
            user_prompt="안녕하세요! 간단히 인사해주세요."
        )

        print("✅ Claude API 연결 성공!")
        print(f"응답: {response[:100]}...")
        print()
        return True

    except Exception as e:
        print(f"❌ Claude API 오류: {str(e)}")
        print()
        return False


def test_gpt():
    """GPT API 테스트"""
    print("=" * 60)
    print("🔍 GPT API 테스트 중...")
    print("=" * 60)

    api_key = os.getenv("OPENAI_API_KEY")

    if not api_key:
        print("❌ OPENAI_API_KEY가 설정되지 않았습니다.")
        print("   .env 파일에 OPENAI_API_KEY를 추가해주세요.")
        return False

    try:
        agent = MultiModelAgent(
            model_type="gpt",
            openai_api_key=api_key,
            temperature=0.7
        )

        response = agent.invoke(
            system_prompt="당신은 도움이 되는 AI 어시스턴트입니다.",
            user_prompt="안녕하세요! 간단히 인사해주세요."
        )

        print("✅ GPT API 연결 성공!")
        print(f"응답: {response[:100]}...")
        print()
        return True

    except Exception as e:
        print(f"❌ GPT API 오류: {str(e)}")
        print()
        return False


if __name__ == "__main__":
    print("\n🚀 API 연결 테스트 시작\n")

    results = {
        "Gemini": test_gemini(),
        "Claude": test_claude(),
        "GPT": test_gpt()
    }

    print("=" * 60)
    print("📊 테스트 결과 요약")
    print("=" * 60)

    for model, success in results.items():
        status = "✅ 성공" if success else "❌ 실패"
        print(f"{model}: {status}")

    print()

    if all(results.values()):
        print("🎉 모든 API가 정상적으로 작동합니다!")
    else:
        print("⚠️  일부 API에 문제가 있습니다. 위의 오류 메시지를 확인하세요.")
        print()
        print("💡 일반적인 해결 방법:")
        print("   1. .env 파일에 올바른 API 키가 설정되어 있는지 확인")
        print("   2. API 키의 할당량이 남아있는지 확인")
        print("   3. 네트워크 연결 확인")
        print("   4. API 키 형식 확인:")
        print("      - Gemini: AIza로 시작")
        print("      - Claude: sk-ant-로 시작")
        print("      - OpenAI: sk-로 시작")

    print()
