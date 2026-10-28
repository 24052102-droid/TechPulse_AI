from datetime import date
from typing import List, Dict, Any
from pydantic import BaseModel, ConfigDict


class DomainTrendPoint(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    date: date
    item_count: int
    avg_impact: float
    wow_delta: float
    is_trending: bool


class DomainSummary(BaseModel):
    domain: str
    item_count_7d: int
    avg_impact_7d: float
    wow_delta: float
    is_trending: bool
    status: str  # "Surging" | "Stable" | "Declining"
    hype_adoption_ratio: float
    history: List[DomainTrendPoint] = []


class TrendsOverviewResponse(BaseModel):
    top_rising_domains: List[DomainSummary]
    all_domains: List[DomainSummary]
    total_active_domains: int
    window: str  # "7d" | "30d"
