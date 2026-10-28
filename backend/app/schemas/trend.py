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


class TrendPointItem(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    domain: str
    date: str
    item_count: int
    avg_impact: float = 5.0
    wow_delta: float = 0.0
    is_trending: bool = False
    hype_adoption_ratio: float = 1.0


class DomainSummary(BaseModel):
    domain: str
    item_count: int = 0
    item_count_7d: int = 0
    avg_impact: float = 5.0
    avg_impact_7d: float = 5.0
    wow_delta: float = 0.0
    is_trending: bool = False
    status: str = "Stable"  # "Surging" | "Stable" | "Declining"
    hype_adoption_ratio: float = 1.0
    history: List[DomainTrendPoint] = []


class TrendsOverviewResponse(BaseModel):
    top_rising_domains: List[DomainSummary]
    all_domains: List[DomainSummary]
    trends: List[TrendPointItem] = []
    total_active_domains: int
    window: str  # "7d" | "30d"
