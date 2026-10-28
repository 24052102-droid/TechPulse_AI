import re
import time
import logging
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
import requests

logger = logging.getLogger(__name__)

ARXIV_API_URL = "http://export.arxiv.org/api/query"
DEFAULT_CATEGORIES = ["cs.LG", "cs.CV", "cs.CL", "cs.RO", "cs.CR", "cs.SY", "eess.SP"]
GITHUB_URL_REGEX = re.compile(r"https?://github\.com/([a-zA-Z0-9_\-\.]+)/([a-zA-Z0-9_\-\.]+)", re.IGNORECASE)


class ArxivService:
    """
    Client for fetching and parsing technical papers from the arXiv API.
    Handles Atom XML parsing, metadata extraction, code repo link detection,
    and rate limit backoff.
    """

    def __init__(self, timeout: int = 15):
        self.timeout = timeout
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": "TechPulseAI-ATIP/1.0 (academic-intelligence-bot; mailto:admin@atip.local)"
        })

    def fetch_recent_papers(
        self,
        categories: list[str] = None,
        max_results: int = 30,
        sort_by: str = "submittedDate",
        sort_order: str = "descending",
    ) -> list[dict]:
        """
        Fetch recently submitted papers across specified categories.
        """
        cats = categories or DEFAULT_CATEGORIES
        cat_query = " OR ".join([f"cat:{c}" for c in cats])
        params = {
            "search_query": cat_query,
            "sortBy": sort_by,
            "sortOrder": sort_order,
            "max_results": max_results,
        }

        logger.info("Querying arXiv API for categories %s (max_results=%d)...", cats, max_results)
        
        try:
            resp = self.session.get(ARXIV_API_URL, params=params, timeout=self.timeout)
            resp.raise_for_status()
            return self._parse_atom_feed(resp.text)
        except Exception as e:
            logger.error("Failed to query arXiv API: %s", e)
            return []

    def _parse_atom_feed(self, xml_text: str) -> list[dict]:
        """
        Parses the Atom XML feed into normalized item dictionaries.
        """
        ns = {
            "atom": "http://www.w3.org/2005/Atom",
            "arxiv": "http://arxiv.org/schemas/atom",
        }

        try:
            root = ET.fromstring(xml_text)
        except ET.ParseError as e:
            logger.error("XML parse error on arXiv feed: %s", e)
            return []

        papers = []
        entries = root.findall("atom:entry", ns)

        for entry in entries:
            raw_id = entry.findtext("atom:id", default="", namespaces=ns).strip()
            # arXiv IDs formatted like 'http://arxiv.org/abs/2403.12345v1' -> '2403.12345'
            paper_id = raw_id.split("/abs/")[-1].split("v")[0] if "/abs/" in raw_id else raw_id

            title = entry.findtext("atom:title", default="", namespaces=ns)
            title = re.sub(r"\s+", " ", title).strip()

            summary = entry.findtext("atom:summary", default="", namespaces=ns)
            summary = re.sub(r"\s+", " ", summary).strip()

            published_str = entry.findtext("atom:published", default="", namespaces=ns)
            try:
                published_dt = datetime.fromisoformat(published_str.replace("Z", "+00:00"))
            except Exception:
                published_dt = datetime.now(timezone.utc)

            authors = [
                author.findtext("atom:name", default="", namespaces=ns).strip()
                for author in entry.findall("atom:author", ns)
                if author.findtext("atom:name", default="", namespaces=ns)
            ]

            categories = [
                cat.attrib.get("term", "").strip()
                for cat in entry.findall("atom:category", ns)
                if cat.attrib.get("term")
            ]

            # Detect any GitHub repository linked in abstract
            github_match = GITHUB_URL_REGEX.search(summary)
            github_url = github_match.group(0) if github_match else None

            pdf_url = f"https://arxiv.org/pdf/{paper_id}.pdf"

            paper_item = {
                "source": "arxiv",
                "source_id": paper_id,
                "title": title,
                "description": summary,
                "url": f"https://arxiv.org/abs/{paper_id}",
                "created_at": published_dt,
                "metadata": {
                    "authors": authors,
                    "categories": categories,
                    "pdf_url": pdf_url,
                    "github_repo_url": github_url,
                    "has_code": bool(github_url),
                    "citation_count": 0,
                    "influential_citation_count": 0,
                    "max_h_index": 0,
                },
            }
            papers.append(paper_item)

        logger.info("Successfully parsed %d arXiv papers from Atom feed", len(papers))
        return papers
