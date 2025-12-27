"""
Agent 5: 퍼블리싱 에이전트
네이버 블로그 및 구글 블로그(Blogger) API를 통해 실제로 게시합니다.
(현재는 스켈레톤 구현)
"""
from typing import Dict, List, Optional
import requests


class PublishResult:
    """퍼블리싱 결과"""
    def __init__(self, success: bool, url: Optional[str] = None, error: Optional[str] = None):
        self.success = success
        self.url = url
        self.error = error

    def to_dict(self):
        return {
            "success": self.success,
            "url": self.url,
            "error": self.error
        }


class NaverBlogPublisher:
    """네이버 블로그 퍼블리셔"""

    def __init__(self, client_id: str, client_secret: str, blog_id: str):
        """
        Args:
            client_id: 네이버 개발자 센터에서 발급받은 클라이언트 ID
            client_secret: 네이버 개발자 센터에서 발급받은 클라이언트 Secret
            blog_id: 블로그 ID
        """
        self.client_id = client_id
        self.client_secret = client_secret
        self.blog_id = blog_id
        self.api_url = "https://openapi.naver.com/blog/writePost.json"

    def publish(
        self,
        title: str,
        content: str,
        image_path: Optional[str] = None
    ) -> PublishResult:
        """
        네이버 블로그에 게시합니다.

        Args:
            title: 게시글 제목
            content: 게시글 내용
            image_path: 이미지 파일 경로 (선택)

        Returns:
            퍼블리싱 결과
        """
        # TODO: 실제 네이버 블로그 API 구현
        # 현재는 스켈레톤만 제공

        print(f"[네이버 블로그] 게시 시도:")
        print(f"  - 제목: {title}")
        print(f"  - 내용 길이: {len(content)}자")
        print(f"  - 이미지: {image_path or '없음'}")

        # 실제 구현 예시 (주석 처리)
        """
        headers = {
            "X-Naver-Client-Id": self.client_id,
            "X-Naver-Client-Secret": self.client_secret
        }

        data = {
            "title": title,
            "contents": content
        }

        if image_path:
            files = {"image": open(image_path, "rb")}
            response = requests.post(self.api_url, headers=headers, data=data, files=files)
        else:
            response = requests.post(self.api_url, headers=headers, data=data)

        if response.status_code == 200:
            result = response.json()
            return PublishResult(success=True, url=result.get("url"))
        else:
            return PublishResult(success=False, error=response.text)
        """

        # 스켈레톤 응답
        return PublishResult(
            success=True,
            url=f"https://blog.naver.com/{self.blog_id}/mock-post-id",
            error=None
        )


class GoogleBloggerPublisher:
    """구글 블로그(Blogger) 퍼블리셔"""

    def __init__(self, api_key: str, blog_id: str, access_token: Optional[str] = None):
        """
        Args:
            api_key: Google API Key
            blog_id: 블로그 ID (예: 123456789012345678)
            access_token: OAuth 2.0 액세스 토큰 (선택, 더 많은 권한 필요 시)
        """
        self.api_key = api_key
        self.blog_id = blog_id
        self.access_token = access_token
        self.api_url = f"https://www.googleapis.com/blogger/v3/blogs/{blog_id}/posts"

    def publish(
        self,
        title: str,
        content: str,
        image_path: Optional[str] = None,
        labels: Optional[List[str]] = None
    ) -> PublishResult:
        """
        구글 블로그에 게시합니다.

        Args:
            title: 게시글 제목
            content: 게시글 내용 (HTML 가능)
            image_path: 이미지 파일 경로 (선택)
            labels: 라벨(태그) 목록

        Returns:
            퍼블리싱 결과
        """
        # TODO: 실제 Google Blogger API 구현

        print(f"[Google Blogger] 게시 시도:")
        print(f"  - 제목: {title}")
        print(f"  - 내용 길이: {len(content)}자")
        print(f"  - 이미지: {image_path or '없음'}")

        # 실제 구현 예시 (주석 처리)
        """
        # 이미지가 있으면 HTML에 포함
        html_content = content
        if image_path:
            # 이미지를 base64로 인코딩하거나 별도 업로드 후 URL 사용
            html_content = f'<img src="{image_path}" /><br>{content}'

        # API 요청 데이터
        post_data = {
            "kind": "blogger#post",
            "blog": {"id": self.blog_id},
            "title": title,
            "content": html_content
        }

        if labels:
            post_data["labels"] = labels

        # 헤더 설정
        headers = {
            "Content-Type": "application/json"
        }

        # OAuth 토큰이 있으면 사용, 없으면 API Key 사용
        if self.access_token:
            headers["Authorization"] = f"Bearer {self.access_token}"
            params = {}
        else:
            params = {"key": self.api_key}

        response = requests.post(
            self.api_url,
            json=post_data,
            headers=headers,
            params=params
        )

        if response.status_code == 200:
            result = response.json()
            post_url = result.get("url")
            return PublishResult(success=True, url=post_url)
        else:
            return PublishResult(success=False, error=response.text)
        """

        # 스켈레톤 응답
        return PublishResult(
            success=True,
            url=f"https://www.blogger.com/blog/post/edit/{self.blog_id}/mock-post-id",
            error=None
        )


class PublisherAgent:
    """통합 퍼블리싱 에이전트"""

    def __init__(
        self,
        naver_config: Optional[Dict] = None,
        google_config: Optional[Dict] = None
    ):
        """
        Args:
            naver_config: 네이버 설정 (client_id, client_secret, blog_id)
            google_config: 구글 블로그 설정 (api_key, blog_id, access_token)
        """
        self.naver = None
        self.google = None

        if naver_config:
            self.naver = NaverBlogPublisher(**naver_config)

        if google_config:
            self.google = GoogleBloggerPublisher(**google_config)

    def publish_to_naver(
        self, title: str, content: str, image_path: Optional[str] = None
    ) -> PublishResult:
        """네이버 블로그에 게시"""
        if not self.naver:
            return PublishResult(success=False, error="네이버 블로그가 설정되지 않았습니다.")
        return self.naver.publish(title, content, image_path)

    def publish_to_google(
        self, title: str, content: str, image_path: Optional[str] = None
    ) -> PublishResult:
        """구글 블로그에 게시"""
        if not self.google:
            return PublishResult(success=False, error="구글 블로그가 설정되지 않았습니다.")
        return self.google.publish(title, content, image_path)

    def publish_all(
        self, title: str, contents: Dict[str, str], image_path: Optional[str] = None
    ) -> List[PublishResult]:
        """
        모든 플랫폼에 게시

        Args:
            title: 게시글 제목
            contents: 플랫폼별 콘텐츠 {"naver": "...", "google": "..."}
            image_path: 이미지 파일 경로

        Returns:
            플랫폼별 퍼블리싱 결과 목록
        """
        results = []

        if "naver" in contents and self.naver:
            result = self.publish_to_naver(title, contents["naver"], image_path)
            results.append(("naver", result))

        if "google" in contents and self.google:
            result = self.publish_to_google(title, contents["google"], image_path)
            results.append(("google", result))

        return results
