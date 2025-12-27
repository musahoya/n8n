"""
Agent 5: 퍼블리싱 에이전트
네이버 블로그 및 티스토리 API를 통해 실제로 게시합니다.
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


class TistoryPublisher:
    """티스토리 퍼블리셔"""

    def __init__(self, access_token: str, blog_name: str):
        """
        Args:
            access_token: 티스토리 OAuth 액세스 토큰
            blog_name: 블로그 이름 (예: myblog.tistory.com의 'myblog')
        """
        self.access_token = access_token
        self.blog_name = blog_name
        self.api_url = "https://www.tistory.com/apis/post/write"

    def publish(
        self,
        title: str,
        content: str,
        image_path: Optional[str] = None,
        category: str = "0"
    ) -> PublishResult:
        """
        티스토리에 게시합니다.

        Args:
            title: 게시글 제목
            content: 게시글 내용 (HTML 가능)
            image_path: 이미지 파일 경로 (선택)
            category: 카테고리 ID

        Returns:
            퍼블리싱 결과
        """
        # TODO: 실제 티스토리 API 구현

        print(f"[티스토리] 게시 시도:")
        print(f"  - 제목: {title}")
        print(f"  - 내용 길이: {len(content)}자")
        print(f"  - 이미지: {image_path or '없음'}")

        # 실제 구현 예시 (주석 처리)
        """
        params = {
            "access_token": self.access_token,
            "blogName": self.blog_name,
            "title": title,
            "content": content,
            "category": category,
            "visibility": "3"  # 0: 비공개, 1: 보호, 3: 발행
        }

        response = requests.post(self.api_url, data=params)

        if response.status_code == 200:
            result = response.json()
            if result.get("tistory", {}).get("status") == "200":
                post_id = result["tistory"]["postId"]
                return PublishResult(
                    success=True,
                    url=f"https://{self.blog_name}.tistory.com/{post_id}"
                )

        return PublishResult(success=False, error=response.text)
        """

        # 스켈레톤 응답
        return PublishResult(
            success=True,
            url=f"https://{self.blog_name}.tistory.com/mock-post-id",
            error=None
        )


class PublisherAgent:
    """통합 퍼블리싱 에이전트"""

    def __init__(
        self,
        naver_config: Optional[Dict] = None,
        tistory_config: Optional[Dict] = None
    ):
        """
        Args:
            naver_config: 네이버 설정 (client_id, client_secret, blog_id)
            tistory_config: 티스토리 설정 (access_token, blog_name)
        """
        self.naver = None
        self.tistory = None

        if naver_config:
            self.naver = NaverBlogPublisher(**naver_config)

        if tistory_config:
            self.tistory = TistoryPublisher(**tistory_config)

    def publish_to_naver(
        self, title: str, content: str, image_path: Optional[str] = None
    ) -> PublishResult:
        """네이버 블로그에 게시"""
        if not self.naver:
            return PublishResult(success=False, error="네이버 블로그가 설정되지 않았습니다.")
        return self.naver.publish(title, content, image_path)

    def publish_to_tistory(
        self, title: str, content: str, image_path: Optional[str] = None
    ) -> PublishResult:
        """티스토리에 게시"""
        if not self.tistory:
            return PublishResult(success=False, error="티스토리가 설정되지 않았습니다.")
        return self.tistory.publish(title, content, image_path)

    def publish_all(
        self, title: str, contents: Dict[str, str], image_path: Optional[str] = None
    ) -> List[PublishResult]:
        """
        모든 플랫폼에 게시

        Args:
            title: 게시글 제목
            contents: 플랫폼별 콘텐츠 {"naver": "...", "tistory": "..."}
            image_path: 이미지 파일 경로

        Returns:
            플랫폼별 퍼블리싱 결과 목록
        """
        results = []

        if "naver" in contents and self.naver:
            result = self.publish_to_naver(title, contents["naver"], image_path)
            results.append(("naver", result))

        if "tistory" in contents and self.tistory:
            result = self.publish_to_tistory(title, contents["tistory"], image_path)
            results.append(("tistory", result))

        return results
