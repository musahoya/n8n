# 🔧 API 오류 수정 가이드

Gemini와 Claude API 오류를 수정했습니다.

## 🐛 발견된 문제

### 1. Gemini API 오류

**문제점**:
- ❌ `model="gemini-1.5-pro"` - 구버전 모델명
- ❌ 시스템 메시지 미지원 이슈

**해결 방법**:
- ✅ `model="gemini-1.5-pro-latest"` - 최신 버전 사용
- ✅ `convert_system_message_to_human=True` 추가

### 2. Claude API 오류

**문제점**:
- ❌ `model="claude-3-5-sonnet-20241022"` - 특정 날짜 버전
- ❌ `anthropic_api_key` - 잘못된 파라미터명
- ❌ `max_tokens=4096` - 낮은 토큰 제한

**해결 방법**:
- ✅ `model="claude-3-5-sonnet-latest"` - 최신 버전 사용
- ✅ `api_key` - 올바른 파라미터명 사용
- ✅ `max_tokens=8192` - Claude 3.5의 최대 출력 토큰

---

## 🔍 수정된 코드

### Before (이전)

```python
# Gemini
return ChatGoogleGenerativeAI(
    model="gemini-1.5-pro",
    google_api_key=gemini_api_key,
    temperature=self.temperature
)

# Claude
return ChatAnthropic(
    model="claude-3-5-sonnet-20241022",
    anthropic_api_key=claude_api_key,
    temperature=self.temperature,
    max_tokens=4096
)
```

### After (수정 후)

```python
# Gemini
return ChatGoogleGenerativeAI(
    model="gemini-1.5-pro-latest",
    google_api_key=gemini_api_key,
    temperature=self.temperature,
    convert_system_message_to_human=True  # 시스템 메시지 변환
)

# Claude
return ChatAnthropic(
    model="claude-3-5-sonnet-latest",
    api_key=claude_api_key,  # 올바른 파라미터명
    temperature=self.temperature,
    max_tokens=8192  # 더 많은 토큰
)
```

---

## 🧪 테스트 방법

### 1. 간단한 테스트

```bash
python test_api.py
```

이 스크립트는 다음을 확인합니다:
- ✅ API 키가 올바르게 설정되었는지
- ✅ 각 모델이 정상적으로 응답하는지
- ✅ 에러 메시지 확인

### 2. Flask 앱으로 테스트

```bash
python app.py
```

웹 브라우저에서 http://localhost:5000 접속 후:
1. API 키 입력
2. 각 단계별로 모델 선택
3. 실제 워크플로우 실행

---

## 💡 일반적인 오류 해결

### 오류 1: "API key not valid"

**원인**: 잘못된 API 키

**해결**:
```bash
# .env 파일 확인
cat .env

# API 키 형식 확인
# Gemini: AIza로 시작
# Claude: sk-ant-로 시작
# OpenAI: sk-로 시작
```

### 오류 2: "Rate limit exceeded"

**원인**: API 할당량 초과

**해결**:
- API 키의 할당량 확인
- 무료 플랜의 경우 제한이 있을 수 있음
- 유료 플랜으로 업그레이드 고려

### 오류 3: "Model not found"

**원인**: 모델명 오류

**해결**:
- ✅ `gemini-1.5-pro-latest` (Gemini)
- ✅ `claude-3-5-sonnet-latest` (Claude)
- ✅ `gpt-4o` (OpenAI)

### 오류 4: "Max tokens exceeded"

**원인**: 출력 토큰 부족

**해결**:
- Claude: `max_tokens=8192`로 증가
- 프롬프트 길이 줄이기

---

## 📊 모델별 스펙

| 모델 | 최대 입력 | 최대 출력 | 비용 |
|------|----------|----------|------|
| **Gemini 1.5 Pro** | 2M 토큰 | 8K 토큰 | 무료/유료 |
| **Claude 3.5 Sonnet** | 200K 토큰 | 8K 토큰 | 유료 |
| **GPT-4o** | 128K 토큰 | 16K 토큰 | 유료 |

---

## 🔐 API 키 발급 재확인

### Gemini
1. https://makersuite.google.com/app/apikey
2. "Create API Key" 클릭
3. 형식: `AIza...`

### Claude
1. https://console.anthropic.com/
2. Settings → API Keys
3. 형식: `sk-ant-...`

### OpenAI
1. https://platform.openai.com/api-keys
2. "Create new secret key"
3. 형식: `sk-...`

---

## ✅ 체크리스트

수정 후 다음을 확인하세요:

- [ ] `.env` 파일에 API 키 설정
- [ ] `test_api.py` 실행하여 연결 테스트
- [ ] Flask 앱 실행 확인
- [ ] 각 모델 선택하여 주제 생성 테스트
- [ ] 콘텐츠 생성 테스트
- [ ] 검수 기능 테스트

---

## 🆘 추가 도움이 필요한 경우

1. **API 키 확인**
   ```bash
   # .env 파일 존재 확인
   ls -la .env

   # 내용 확인 (민감 정보 주의)
   cat .env
   ```

2. **패키지 버전 확인**
   ```bash
   pip list | grep langchain
   pip list | grep google
   pip list | grep anthropic
   ```

3. **재설치**
   ```bash
   pip install --upgrade langchain-google-genai
   pip install --upgrade langchain-anthropic
   pip install --upgrade langchain-openai
   ```

---

**모든 수정이 완료되었습니다!** 🎉

이제 `python test_api.py`를 실행하여 API 연결을 테스트하세요.
