# 🏗️ 시스템 아키텍처 상세 설명

## 목차

1. [전체 시스템 구조](#1-전체-시스템-구조)
2. [에이전트별 상세 설계](#2-에이전트별-상세-설계)
3. [상태 관리 시스템](#3-상태-관리-시스템)
4. [LangGraph 워크플로우](#4-langgraph-워크플로우)
5. [확장 가능한 설계](#5-확장-가능한-설계)

---

## 1. 전체 시스템 구조

### 1.1 시스템 개요

이 시스템은 **파이프라인(Pipeline)** 방식이 아니라 **상태 기반(State-based)** 워크플로우입니다.

- ❌ **파이프라인 방식**: Agent 1 → Agent 2 → Agent 3 (일방향)
- ✅ **상태 기반 방식**: 공유 상태를 중심으로 에이전트가 협업

### 1.2 핵심 설계 원칙

1. **단일 진실 공급원(Single Source of Truth)**
   - 모든 데이터는 `WorkflowState`에 저장
   - 각 에이전트는 상태를 읽고 업데이트

2. **느슨한 결합(Loose Coupling)**
   - 에이전트는 서로를 직접 호출하지 않음
   - LangGraph가 흐름을 관리

3. **확장성(Extensibility)**
   - 새로운 에이전트를 쉽게 추가 가능
   - 조건부 분기 및 루프 지원

---

## 2. 에이전트별 상세 설계

### 2.1 Agent 1: 기획자 (Gemini)

**책임**: 업종 분석 및 블로그 주제 추천

**입력**:
```python
{
    "business_type": "세무사"
}
```

**출력**:
```python
{
    "topic_suggestions": [
        {
            "keyword": "종합소득세 절세",
            "title": "세무사가 알려주는 종합소득세 절세 꿀팁",
            "reason": "5월 신고 시즌 검색량 급증"
        }
    ]
}
```

**주요 기능**:
- Google Search Tool 활용 (향후 구현)
- 계절성 키워드 분석
- 경쟁 강도 평가

**왜 Gemini인가?**
- 구글 검색과의 통합이 우수
- 최신 트렌드 파악 능력
- 다양한 관점에서 주제 제안

---

### 2.2 Agent 2: 작가 (Claude)

**책임**: 플랫폼별 맞춤 콘텐츠 작성

**입력**:
```python
{
    "selected_topic": {
        "keyword": "종합소득세 절세",
        "title": "...",
        "reason": "..."
    },
    "business_type": "세무사"
}
```

**출력**:
```python
{
    "content_versions": [
        {
            "platform": "naver",
            "content": "안녕하세요! 😊 ...",
            "tone": "friendly"
        },
        {
            "platform": "tistory",
            "content": "## 종합소득세란?\n...",
            "tone": "professional"
        }
    ]
}
```

**플랫폼별 전략**:

| 플랫폼 | 톤 | 구조 | 특징 |
|--------|-----|------|------|
| 네이버 | 친근함 | 짧은 문단, 이모지 | 카카오톡처럼 편안하게 |
| 티스토리 | 전문적 | 명확한 소제목, 리스트 | 정보 전달 중심 |
| 구글 | 객관적 | H2/H3 태그, SEO 키워드 | 검색 최적화 |

**왜 Claude인가?**
- 가장 자연스러운 한국어 문체
- 톤앤매너 조절 능력 탁월
- 긴 문맥 이해 (200K 토큰)

---

### 2.3 Agent 3: 편집자 (GPT-4o) [예정]

**책임**: 팩트 체크 및 품질 검수

**검수 항목**:
1. **사실 정확성**: 법률/세무 정보가 정확한가?
2. **맞춤법**: 오타나 문법 오류가 없는가?
3. **광고성 문구**: 과도한 홍보 표현이 있는가?
4. **금칙어**: 부적절한 표현이 포함되어 있는가?

**조건부 라우팅**:
```python
if review_passed:
    → Agent 4 (이미지 생성)
else:
    → Agent 2 (재작성)
```

**최대 재시도**: 2회

**왜 GPT-4o인가?**
- 지시 사항 준수 능력이 가장 엄격
- 논리적 오류 탐지에 강함
- 빠른 응답 속도

---

### 2.4 Agent 4: 이미지 생성 (DALL-E 3) [예정]

**책임**: 블로그 썸네일 이미지 생성

**프로세스**:
1. 콘텐츠 분석
2. 이미지 프롬프트 생성 (GPT-4o)
3. DALL-E 3로 이미지 생성
4. URL 반환

**예시 프롬프트**:
```
A professional illustration of Korean tax documents
with calculator and pen, clean modern style,
minimalist design, pastel colors
```

---

### 2.5 Agent 5: 퍼블리셔 (Python API) [예정]

**책임**: 실제 블로그에 자동 게시

**지원 플랫폼**:
- 네이버 블로그 API
- 티스토리 API

**기능**:
- 자동 게시
- 예약 발행
- 카테고리 자동 분류

---

## 3. 상태 관리 시스템

### 3.1 WorkflowState 구조

```python
class WorkflowState(TypedDict):
    # === 사용자 입력 ===
    business_type: str

    # === Agent 1 출력 ===
    topic_suggestions: Optional[List[TopicSuggestion]]
    selected_topic: Optional[TopicSuggestion]

    # === Agent 2 출력 ===
    content_versions: Optional[List[ContentVersion]]

    # === Agent 3 출력 ===
    review_passed: Optional[bool]
    review_feedback: Optional[str]

    # === Agent 4 출력 ===
    image_prompt: Optional[str]
    image_url: Optional[str]

    # === Agent 5 출력 ===
    published_urls: Optional[List[str]]

    # === 제어 변수 ===
    retry_count: int
    current_step: str
```

### 3.2 상태 전이

```
초기 상태:
{
    "business_type": "세무사",
    "retry_count": 0,
    "current_step": "planning"
}

↓ Agent 1 실행 후

{
    "business_type": "세무사",
    "topic_suggestions": [...],
    "current_step": "topic_selection"
}

↓ 주제 선택 후

{
    "selected_topic": {...},
    "current_step": "writing"
}

↓ Agent 2 실행 후

{
    "content_versions": [...],
    "current_step": "content_review"
}
```

---

## 4. LangGraph 워크플로우

### 4.1 현재 워크플로우 (v0.1)

```python
START
  ↓
planner (Agent 1)
  ↓
topic_selection
  ↓
writer (Agent 2)
  ↓
END
```

### 4.2 고급 워크플로우 (v1.0 예정)

```python
START
  ↓
planner
  ↓
topic_selection
  ↓
writer
  ↓
reviewer ──┐
  ↓        │
  ↓ (통과)  │ (실패, retry_count < 2)
  ↓        │
  ↓ ←──────┘
image_generator
  ↓
publisher
  ↓
END
```

### 4.3 조건부 분기 코드

```python
workflow.add_conditional_edges(
    "reviewer",
    should_retry,  # 조건 함수
    {
        "retry": "writer",      # 재작성
        "continue": "image_generator"  # 다음 단계
    }
)

def should_retry(state: WorkflowState) -> Literal["retry", "continue"]:
    if state["retry_count"] >= 2:
        return "continue"  # 강제 진행

    if not state["review_passed"]:
        state["retry_count"] += 1
        return "retry"  # 재작성

    return "continue"
```

---

## 5. 확장 가능한 설계

### 5.1 새로운 에이전트 추가 방법

1. **에이전트 클래스 생성**:
```python
# agent_seo_optimizer.py
class SEOOptimizerAgent:
    def optimize(self, state: WorkflowState) -> WorkflowState:
        # SEO 최적화 로직
        return state
```

2. **노드 함수 정의**:
```python
def seo_node(state: WorkflowState) -> WorkflowState:
    agent = SEOOptimizerAgent()
    return agent.optimize(state)
```

3. **워크플로우에 추가**:
```python
workflow.add_node("seo_optimizer", seo_node)
workflow.add_edge("writer", "seo_optimizer")
workflow.add_edge("seo_optimizer", "reviewer")
```

### 5.2 병렬 실행 지원

여러 에이전트를 동시에 실행:

```python
from langgraph.graph import parallel

workflow.add_node("parallel_processing", parallel(
    image_generator_node,
    seo_optimizer_node,
    metadata_generator_node
))
```

### 5.3 커스텀 조건 분기

```python
def route_by_quality(state: WorkflowState) -> str:
    score = state.get("quality_score", 0)

    if score >= 90:
        return "publish"
    elif score >= 70:
        return "minor_edit"
    else:
        return "rewrite"

workflow.add_conditional_edges(
    "reviewer",
    route_by_quality,
    {
        "publish": "publisher",
        "minor_edit": "editor",
        "rewrite": "writer"
    }
)
```

---

## 6. 성능 최적화

### 6.1 캐싱 전략

```python
from functools import lru_cache

@lru_cache(maxsize=100)
def get_trending_keywords(business_type: str):
    # 같은 업종에 대한 중복 요청 방지
    pass
```

### 6.2 비동기 실행

```python
import asyncio

async def parallel_content_generation(topic):
    tasks = [
        generate_naver_content(topic),
        generate_tistory_content(topic),
        generate_google_content(topic)
    ]
    return await asyncio.gather(*tasks)
```

---

## 7. 에러 처리

### 7.1 재시도 로직

```python
from tenacity import retry, stop_after_attempt, wait_exponential

@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=2, max=10)
)
def call_llm(prompt):
    # API 호출
    pass
```

### 7.2 Fallback 전략

```python
def writer_node_with_fallback(state):
    try:
        return claude_writer(state)
    except Exception:
        # Claude 실패 시 GPT-4로 대체
        return gpt4_writer(state)
```

---

## 8. 모니터링 및 로깅

### 8.1 구조화된 로깅

```python
import logging

logger = logging.getLogger(__name__)

def planner_node(state):
    logger.info(
        "Agent 1 시작",
        extra={
            "business_type": state["business_type"],
            "timestamp": datetime.now()
        }
    )
    # ...
```

### 8.2 실행 시간 측정

```python
import time

def track_execution_time(func):
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        elapsed = time.time() - start
        print(f"{func.__name__} 실행 시간: {elapsed:.2f}초")
        return result
    return wrapper
```

---

이 아키텍처 문서는 시스템의 현재 상태와 향후 확장 방향을 모두 다룹니다.
질문이나 제안 사항이 있으시면 언제든지 Issue를 등록해주세요! 🚀
