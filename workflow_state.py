"""
멀티 에이전트 워크플로우의 상태 정의
각 에이전트 간에 전달되는 데이터 구조를 정의합니다.
"""
from typing import TypedDict, List, Optional
from pydantic import BaseModel


class TopicSuggestion(BaseModel):
    """주제 제안 데이터 모델"""
    keyword: str
    title: str
    reason: str


class ContentVersion(BaseModel):
    """플랫폼별 콘텐츠 버전"""
    platform: str  # "naver", "tistory", "google"
    content: str
    tone: str  # "friendly", "professional", "casual"


class WorkflowState(TypedDict):
    """워크플로우 전체 상태"""
    # Input
    business_type: str  # 사용자가 입력한 업종 (예: "세무사")

    # Agent 1 (Gemini) Output
    topic_suggestions: Optional[List[TopicSuggestion]]  # 추천된 주제 목록
    selected_topic: Optional[TopicSuggestion]  # 사용자가 선택한 주제

    # Agent 2 (Claude) Output
    content_versions: Optional[List[ContentVersion]]  # 플랫폼별 작성된 글

    # Agent 3 (GPT-4o) Output
    review_passed: Optional[bool]  # 검수 통과 여부
    review_feedback: Optional[str]  # 검수 피드백

    # Agent 4 (GPT-4o + DALL-E) Output
    image_prompt: Optional[str]  # 생성된 이미지 프롬프트
    image_url: Optional[str]  # 생성된 이미지 URL

    # Final Output
    published_urls: Optional[List[str]]  # 퍼블리싱된 URL 목록

    # Workflow Control
    retry_count: int  # Agent 3에서 다시 Agent 2로 돌아간 횟수
    current_step: str  # 현재 진행 중인 단계
