"""
External Service Integrations for ATIP (TechPulse AI)
- ArxivService: arXiv API ingestion & Atom XML parsing
- GitHubService: GitHub REST API repository search & README retrieval
- HNService: Hacker News Algolia API intelligence ingestion
- SemanticScholarService: Academic citation & author metrics enrichment
- LLMService: Claude 3.5 Sonnet / LLM insight synthesis with Redis caching
"""

from backend.app.services.arxiv_service import ArxivService
from backend.app.services.github_service import GitHubService
from backend.app.services.hn_service import HNService
from backend.app.services.semantic_scholar_service import SemanticScholarService
from backend.app.services.llm_service import LLMService

__all__ = [
    "ArxivService",
    "GitHubService",
    "HNService",
    "SemanticScholarService",
    "LLMService",
]
