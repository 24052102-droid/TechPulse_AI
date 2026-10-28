import logging
from datetime import datetime, timezone
import requests

logger = logging.getLogger(__name__)

HN_ALGOLIA_URL = "https://hn.algolia.com/api/v1/search"
DEFAULT_KEYWORDS = ["machine learning", "LLM", "neural network", "open source AI", "computer vision"]


class HNService:
    """
    Client for fetching high-signal tech discussions from Hacker News via the Algolia API.
    Filters stories by engagement (points >= 20) and technical relevance.
    """

    def __init__(self, timeout: int = 15):
        self.timeout = timeout
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": "TechPulseAI-ATIP/1.0",
        })

    def fetch_top_tech_stories(
        self,
        keyword: str = "machine learning",
        min_points: int = 20,
        max_results: int = 30,
    ) -> list[dict]:
        """
        Queries Hacker News Algolia API for stories matching keywords and minimum points.
        """
        params = {
            "query": keyword,
            "tags": "story",
            "numericFilters": f"points>={min_points}",
            "hitsPerPage": min(max_results, 50),
        }

        logger.info("Querying HN Algolia API for '%s' (min_points=%d)...", keyword, min_points)

        try:
            resp = self.session.get(HN_ALGOLIA_URL, params=params, timeout=self.timeout)
            resp.raise_for_status()
            data = resp.json()
            hits = data.get("hits", [])
            logger.info("HN Algolia returned %d stories", len(hits))
            return self._normalize_stories(hits[:max_results])
        except Exception as e:
            logger.error("HN Algolia search failed: %s", e)
            return []

    def _normalize_stories(self, raw_hits: list[dict]) -> list[dict]:
        normalized = []
        for h in raw_hits:
            story_id = str(h.get("objectID", ""))
            title = h.get("title", "")
            if not story_id or not title:
                continue

            url = h.get("url") or f"https://news.ycombinator.com/item?id={story_id}"
            description = h.get("story_text") or f"Hacker News discussion on: {title}"

            created_str = h.get("created_at")
            try:
                created_dt = datetime.fromisoformat(created_str.replace("Z", "+00:00")) if created_str else datetime.now(timezone.utc)
            except Exception:
                created_dt = datetime.now(timezone.utc)

            points = int(h.get("points", 0))
            num_comments = int(h.get("num_comments", 0))

            norm_item = {
                "source": "hn",
                "source_id": story_id,
                "title": title,
                "description": description[:600],
                "url": url,
                "created_at": created_dt,
                "metadata": {
                    "points": points,
                    "num_comments": num_comments,
                    "author": h.get("author", "unknown"),
                    "hn_discussion_url": f"https://news.ycombinator.com/item?id={story_id}",
                    "velocity_score": round(points / max(1.0, (datetime.now(timezone.utc) - created_dt).total_seconds() / 3600.0), 2),
                },
            }
            normalized.append(norm_item)
        return normalized
