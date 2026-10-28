import logging
import requests
from backend.app.core.config import settings

logger = logging.getLogger(__name__)

S2_API_URL = "https://api.semanticscholar.org/graph/v1/paper"


class SemanticScholarService:
    """
    Client for enriching academic papers with citation counts and author h-index metrics
    using the Semantic Scholar Graph API.
    """

    def __init__(self, timeout: int = 15):
        self.timeout = timeout
        self.session = requests.Session()
        headers = {
            "User-Agent": "TechPulseAI-ATIP/1.0",
        }
        if settings.SEMANTIC_SCHOLAR_API_KEY:
            headers["x-api-key"] = settings.SEMANTIC_SCHOLAR_API_KEY
        self.session.headers.update(headers)

    def get_paper_enrichment(self, arxiv_id: str) -> dict:
        """
        Enriches a single arXiv paper ID with citation count and author h-index.
        """
        clean_id = arxiv_id.split("v")[0] if "v" in arxiv_id else arxiv_id
        url = f"{S2_API_URL}/arXiv:{clean_id}"
        params = {
            "fields": "citationCount,influentialCitationCount,authors.hIndex,year"
        }

        try:
            resp = self.session.get(url, params=params, timeout=self.timeout)
            if resp.status_code == 200:
                data = resp.json()
                authors = data.get("authors") or []
                h_indices = [a.get("hIndex", 0) for a in authors if a and a.get("hIndex") is not None]
                max_h = max(h_indices) if h_indices else 0

                return {
                    "citation_count": int(data.get("citationCount") or 0),
                    "influential_citation_count": int(data.get("influentialCitationCount") or 0),
                    "max_h_index": max_h,
                    "year": data.get("year"),
                }
            elif resp.status_code == 404:
                logger.debug("Paper arXiv:%s not found in Semantic Scholar index", clean_id)
            elif resp.status_code == 429:
                logger.warning("Semantic Scholar rate limit reached")
        except Exception as e:
            logger.debug("Failed to enrich paper arXiv:%s: %s", clean_id, e)

        return {
            "citation_count": 0,
            "influential_citation_count": 0,
            "max_h_index": 0,
            "year": None,
        }

    def batch_enrich_papers(self, arxiv_ids: list[str]) -> dict[str, dict]:
        """
        Enriches multiple papers using the Semantic Scholar batch API.
        Returns a mapping from clean arxiv_id to enrichment dictionary.
        """
        if not arxiv_ids:
            return {}

        url = f"{S2_API_URL}/batch"
        params = {
            "fields": "citationCount,influentialCitationCount,authors.hIndex,year"
        }
        clean_map = {f"ARXIV:{aid.split('v')[0]}": aid for aid in arxiv_ids}
        payload = {"ids": list(clean_map.keys())}

        results = {}
        try:
            resp = self.session.post(url, json=payload, params=params, timeout=self.timeout)
            if resp.status_code == 200:
                data_list = resp.json()
                for req_key, data in zip(payload["ids"], data_list):
                    orig_id = clean_map.get(req_key, req_key.replace("ARXIV:", ""))
                    if data:
                        authors = data.get("authors") or []
                        h_indices = [a.get("hIndex", 0) for a in authors if a and a.get("hIndex") is not None]
                        results[orig_id] = {
                            "citation_count": int(data.get("citationCount") or 0),
                            "influential_citation_count": int(data.get("influentialCitationCount") or 0),
                            "max_h_index": max(h_indices) if h_indices else 0,
                        }
                    else:
                        results[orig_id] = {"citation_count": 0, "influential_citation_count": 0, "max_h_index": 0}
                return results
        except Exception as e:
            logger.warning("Semantic Scholar batch enrichment failed: %s. Falling back to default metrics.", e)

        for aid in arxiv_ids:
            results[aid] = {"citation_count": 0, "influential_citation_count": 0, "max_h_index": 0}
        return results
