import base64
import logging
from datetime import datetime, timedelta, timezone
import requests
from backend.app.core.config import settings

logger = logging.getLogger(__name__)

GITHUB_API_URL = "https://api.github.com"
DEFAULT_TOPICS = ["machine-learning", "deep-learning", "llm", "reinforcement-learning", "computer-vision"]


class GitHubService:
    """
    Client for fetching active and trending technical repositories via the GitHub REST API.
    Handles rate-limit detection, token authentication, and README content retrieval.
    """

    def __init__(self, timeout: int = 15):
        self.timeout = timeout
        self.session = requests.Session()
        headers = {
            "Accept": "application/vnd.github.v3+json",
            "User-Agent": "TechPulseAI-ATIP/1.0",
        }
        if settings.GITHUB_PAT:
            headers["Authorization"] = f"Bearer {settings.GITHUB_PAT}"
        self.session.headers.update(headers)

    def fetch_trending_repos(
        self,
        min_stars: int = 100,
        days_back: int = 3,
        topic: str = "machine-learning",
        max_results: int = 30,
    ) -> list[dict]:
        """
        Queries GitHub Search API for repositories matching topic, minimum stars,
        and recent push activity.
        """
        since_date = (datetime.now(timezone.utc) - timedelta(days=days_back)).strftime("%Y-%m-%d")
        query = f"stars:>{min_stars} pushed:>{since_date} topic:{topic}"

        url = f"{GITHUB_API_URL}/search/repositories"
        params = {
            "q": query,
            "sort": "updated",
            "order": "desc",
            "per_page": min(max_results, 100),
        }

        logger.info("Querying GitHub API for '%s' (max_results=%d)...", query, max_results)

        try:
            resp = self.session.get(url, params=params, timeout=self.timeout)
            if resp.status_code == 403:
                logger.warning("GitHub API rate limit reached: %s", resp.json().get("message"))
                return []
            resp.raise_for_status()
            data = resp.json()
            items = data.get("items", [])
            logger.info("GitHub search returned %d repositories", len(items))
            return self._normalize_repos(items[:max_results])
        except Exception as e:
            logger.error("GitHub search failed: %s", e)
            return []

    def fetch_readme_snippet(self, full_name: str, max_chars: int = 600) -> str:
        """
        Fetches the initial snippet of the repository's README.
        """
        url = f"{GITHUB_API_URL}/repos/{full_name}/readme"
        try:
            resp = self.session.get(url, timeout=5)
            if resp.status_code == 200:
                content = resp.json().get("content", "")
                decoded = base64.b64decode(content).decode("utf-8", errors="ignore")
                # Remove Markdown images and extra whitespace
                cleaned = " ".join(decoded.split())
                return cleaned[:max_chars]
        except Exception as e:
            logger.debug("Could not fetch README for %s: %s", full_name, e)
        return ""

    def _normalize_repos(self, raw_items: list[dict]) -> list[dict]:
        normalized = []
        for r in raw_items:
            full_name = r.get("full_name", "")
            description = r.get("description") or f"Open-source repository: {full_name}"

            license_info = r.get("license") or {}
            license_name = license_info.get("spdx_id") or license_info.get("name") or "none"

            created_str = r.get("created_at")
            try:
                created_dt = datetime.fromisoformat(created_str.replace("Z", "+00:00")) if created_str else datetime.now(timezone.utc)
            except Exception:
                created_dt = datetime.now(timezone.utc)

            pushed_str = r.get("pushed_at")
            try:
                pushed_dt = datetime.fromisoformat(pushed_str.replace("Z", "+00:00")) if pushed_str else datetime.now(timezone.utc)
            except Exception:
                pushed_dt = datetime.now(timezone.utc)

            norm_item = {
                "source": "github",
                "source_id": full_name,
                "title": full_name,
                "description": description,
                "url": r.get("html_url", f"https://github.com/{full_name}"),
                "created_at": created_dt,
                "metadata": {
                    "stargazers_count": int(r.get("stargazers_count", 0)),
                    "forks_count": int(r.get("forks_count", 0)),
                    "open_issues_count": int(r.get("open_issues_count", 0)),
                    "language": r.get("language") or "Python",
                    "license": license_name,
                    "topics": r.get("topics", []),
                    "pushed_at": pushed_dt.isoformat(),
                    "readme_snippet": description[:600],
                },
            }
            normalized.append(norm_item)
        return normalized
