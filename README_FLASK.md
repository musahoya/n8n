# 🤖 멀티 에이전트 워크플로우 시스템 (Flask 웹 버전)

Flask 기반의 웹 인터페이스로 AI 에이전트를 직관적으로 사용할 수 있는 블로그 자동화 시스템입니다.

## ✨ 주요 특징

### 🎨 **유연한 모델 선택**
- 각 단계마다 원하는 AI 모델을 자유롭게 선택 가능
- Agent 1 (주제 기획): Gemini / Claude / GPT
- Agent 2 (글 작성): Gemini / Claude / GPT
- Agent 3 (검수): Gemini / Claude / GPT
- Agent 4 (이미지 프롬프트): Gemini 고정

### 📸 **사용자 주도 이미지 업로드**
- DALL-E 대신 Gemini가 이미지 프롬프트만 생성
- 사용자가 직접 이미지를 선택하고 업로드
- DALL-E, Midjourney, Stable Diffusion 등 어떤 도구든 사용 가능

### 🚀 **완전한 워크플로우**
1. **설정**: API 키 및 각 단계별 모델 선택
2. **업종 입력**: 블로그 주제와 관련된 업종 입력
3. **주제 선택**: AI가 추천한 5개 주제 중 선택
4. **콘텐츠 생성**: 네이버/티스토리/구글 플랫폼별 맞춤 글 생성
5. **검수**: AI가 품질 검증 (70점 이상 통과)
6. **이미지 추가**: AI 프롬프트 참고하여 이미지 업로드
7. **미리보기 & 발행**: 최종 확인 후 퍼블리싱

---

## 📦 설치 방법

### 1. 저장소 클론

```bash
git clone <repository-url>
cd n8n
```

### 2. Python 가상환경 생성

```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

### 3. 의존성 설치

```bash
pip install -r requirements.txt
```

### 4. Flask 앱 실행

```bash
python app.py
```

웹 브라우저에서 http://localhost:5000 접속

---

## 🎯 사용 방법

### Step 0: 초기 설정

1. 웹 브라우저에서 http://localhost:5000 접속
2. API 키 입력:
   - Google Gemini API Key (필수 - 이미지 프롬프트 생성에 사용)
   - Anthropic Claude API Key (선택)
   - OpenAI GPT API Key (선택)
   - 최소 1개 이상 입력
3. 각 단계별 AI 모델 선택:
   - **Agent 1 (주제 기획)**: Gemini 추천 (검색 능력 우수)
   - **Agent 2 (글 작성)**: Claude 추천 (자연스러운 한국어)
   - **Agent 3 (검수)**: GPT 추천 (엄격한 검수)
4. 퍼블리싱 설정 (선택사항):
   - 네이버 블로그 API 설정
   - 티스토리 API 설정

### Step 1: 업종 입력

- 예시: "세무사", "변호사", "프랜차이즈 카페", "성형외과"
- 구체적일수록 좋음

### Step 2: 주제 선택

- AI가 추천한 5개 주제 중 하나 선택
- 각 주제는 키워드, 제목, 추천 이유 포함

### Step 3: 콘텐츠 생성

- 네이버 블로그, 티스토리, 구글 블로그용 3가지 버전 생성
- 각 플랫폼의 특성에 맞게 톤과 구조가 다름
- 원하는 플랫폼 선택

### Step 4: 검수

- AI가 자동으로 품질 검수 (0-100점)
- 70점 이상이면 통과
- 불합격 시 다시 작성하거나 그대로 진행 가능

### Step 5: 이미지 추가

- AI가 생성한 영문 프롬프트 확인
- 프롬프트를 복사하여 DALL-E, Midjourney 등에서 이미지 생성
- 생성한 이미지 업로드

### Step 6: 최종 미리보기 & 발행

- 제목, 본문, 이미지 최종 확인
- 발행 버튼 클릭 → 자동 퍼블리싱

---

## 🏗️ 프로젝트 구조

```
n8n/
├── app.py                          # Flask 메인 애플리케이션
├── multi_model_agent.py            # 멀티 모델 지원 기반 클래스
├── agents/                         # 에이전트 모듈
│   ├── __init__.py
│   ├── planner_agent.py           # Agent 1: 주제 기획
│   ├── writer_agent.py            # Agent 2: 콘텐츠 작성
│   ├── reviewer_agent.py          # Agent 3: 검수
│   ├── image_prompt_agent.py      # Agent 4: 이미지 프롬프트
│   └── publisher_agent.py         # Agent 5: 퍼블리싱
├── templates/                      # HTML 템플릿
│   ├── base.html                  # 기본 레이아웃
│   ├── index.html                 # 설정 페이지
│   ├── step1_business_type.html   # Step 1
│   ├── step2_topic_selection.html # Step 2
│   ├── step3_content_display.html # Step 3
│   ├── step4_review.html          # Step 4
│   ├── step5_image_upload.html    # Step 5
│   ├── step6_preview.html         # Step 6
│   └── publish_result.html        # 발행 결과
├── static/                         # 정적 파일
│   ├── css/
│   │   └── style.css              # 스타일시트
│   └── uploads/                   # 업로드된 이미지 저장
├── requirements.txt                # Python 의존성
└── README_FLASK.md                # 이 파일
```

---

## 🤝 에이전트 상세

### Agent 1: 주제 기획 (PlannerAgentMultiModel)

**목적**: 업종을 분석하여 블로그 주제 추천

**입력**:
- business_type: 업종 (예: "세무사")
- model_type: "gemini" | "claude" | "gpt"

**출력**:
- 5개의 주제 추천 (키워드, 제목, 이유)

**추천 모델**: Gemini (검색 능력 우수, 트렌드 파악)

---

### Agent 2: 콘텐츠 작성 (WriterAgentMultiModel)

**목적**: 플랫폼별 맞춤 블로그 글 작성

**입력**:
- 선택된 주제
- model_type: "gemini" | "claude" | "gpt"

**출력**:
- 네이버 블로그용 (친근한 톤, 이모지)
- 티스토리용 (전문적, 구조화)
- 구글 블로그용 (SEO 최적화)

**추천 모델**: Claude (자연스러운 한국어, 톤앤매너 조절)

---

### Agent 3: 검수 (ReviewerAgentMultiModel)

**목적**: 팩트 체크 및 품질 검수

**입력**:
- 작성된 콘텐츠
- model_type: "gemini" | "claude" | "gpt"

**출력**:
- passed: True/False
- score: 0-100점
- feedback: 구체적인 피드백

**검수 기준**:
1. 사실 정확성 (30점)
2. 맞춤법/문법 (20점)
3. 콘텐츠 품질 (30점)
4. 부적절한 내용 (20점)

**추천 모델**: GPT-4o (엄격한 지시 이행, 논리적 검증)

---

### Agent 4: 이미지 프롬프트 (ImagePromptAgent)

**목적**: 블로그 이미지용 프롬프트 생성

**입력**:
- 콘텐츠
- 키워드

**출력**:
- 영문 이미지 생성 프롬프트

**고정 모델**: Gemini (창의적인 프롬프트 생성)

**사용자 작업**:
1. 프롬프트 복사
2. DALL-E/Midjourney/Stable Diffusion에서 이미지 생성
3. 생성한 이미지 업로드

---

### Agent 5: 퍼블리싱 (PublisherAgent)

**목적**: 네이버/티스토리에 자동 게시

**지원 플랫폼**:
- 네이버 블로그 (API 연동 필요)
- 티스토리 (OAuth 토큰 필요)

**현재 상태**: 스켈레톤 구현 (테스트 모드)

**실제 사용**:
`agents/publisher_agent.py`의 주석 처리된 API 코드를 활성화하세요.

---

## 🎨 플랫폼별 콘텐츠 특징

| 플랫폼 | 톤 | 구조 | 특징 |
|--------|-----|------|------|
| **네이버** | 친근함 | 짧은 문단, 이모지 | 카카오톡처럼 대화하듯 |
| **티스토리** | 전문적 | 명확한 소제목, 리스트 | 정보 전달 중심 |
| **구글** | 객관적 | H2/H3 태그, SEO 키워드 | 검색 엔진 최적화 |

---

## 🔑 API 키 발급 방법

### Google Gemini
1. https://makersuite.google.com/app/apikey 접속
2. Google 계정으로 로그인
3. "Create API Key" 클릭
4. API 키 복사

### Anthropic Claude
1. https://console.anthropic.com/ 접속
2. 계정 생성/로그인
3. "API Keys" 메뉴에서 발급
4. API 키 복사

### OpenAI GPT
1. https://platform.openai.com/api-keys 접속
2. 계정 생성/로그인
3. "Create new secret key" 클릭
4. API 키 복사

---

## 🚨 퍼블리싱 설정 (고급)

### 네이버 블로그 API

1. https://developers.naver.com/ 접속
2. 애플리케이션 등록
3. 블로그 API 사용 설정
4. Client ID, Client Secret 발급
5. 웹 UI에서 입력

### 티스토리 API

1. https://www.tistory.com/guide/api/manage/register 접속
2. 앱 등록
3. OAuth 인증
4. Access Token 발급
5. 웹 UI에서 입력

---

## 💡 사용 팁

### 모델 선택 가이드

**비용 절감형**:
- Agent 1: Gemini (무료 할당량 많음)
- Agent 2: Gemini
- Agent 3: Gemini

**품질 최우선형**:
- Agent 1: Gemini (검색 능력)
- Agent 2: Claude (최고의 한국어)
- Agent 3: GPT-4o (엄격한 검수)

**균형형** (추천):
- Agent 1: Gemini
- Agent 2: Claude
- Agent 3: GPT

### 검수 점수 기준

- **90점 이상**: 출판 가능한 완성도
- **70-89점**: 약간의 수정 필요
- **70점 미만**: 재작성 권장

---

## 🛠️ 기술 스택

- **Backend**: Flask 3.0
- **AI 모델**:
  - Google Gemini 1.5 Pro
  - Anthropic Claude 3.5 Sonnet
  - OpenAI GPT-4o
- **프레임워크**: LangChain 0.3
- **프론트엔드**: HTML5, CSS3, JavaScript (Vanilla)
- **이미지 처리**: Pillow

---

## 🐛 트러블슈팅

### API 키 오류
- API 키가 올바른지 확인
- 할당량이 남아있는지 확인
- 네트워크 연결 확인

### 이미지 업로드 실패
- 파일 크기 확인 (최대 16MB)
- 지원 형식 확인 (PNG, JPG, GIF, WEBP)

### 퍼블리싱 실패
- 현재는 테스트 모드입니다
- 실제 API 연동을 위해 `publisher_agent.py` 수정 필요

---

## 📝 라이선스

MIT License

---

## 🙋 문의 및 기여

- Issue: 문제 보고 및 기능 제안
- Pull Request: 코드 기여 환영

---

## 🎉 변경사항 (vs CLI 버전)

### ✅ 개선된 점

1. **웹 UI**: 직관적인 단계별 인터페이스
2. **모델 선택**: 각 단계마다 AI 모델 자유 선택
3. **이미지 업로드**: 사용자가 직접 이미지 관리
4. **실시간 미리보기**: 발행 전 최종 확인
5. **세션 관리**: 진행 상황 자동 저장

### 🔄 변경된 점

- CLI → Flask 웹 애플리케이션
- 고정 모델 → 유연한 모델 선택
- DALL-E 자동 생성 → Gemini 프롬프트 + 수동 업로드
- LangGraph 워크플로우 → Flask 라우팅

---

**Happy Blogging! 🚀**
