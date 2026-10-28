from datetime import datetime
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, ConfigDict


class DriverFeature(BaseModel):
    feature: str
    value: Any
    impact: float


class ItemCardResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    source: str
    source_id: str
    title: str
    description: Optional[str] = None
    url: str
    primary_domain: Optional[str] = "General Machine Learning"
    secondary_domains: List[str] = []
    domain_confidence: Optional[float] = 0.8
    impact_score: Optional[float] = 5.0  # 0.0 to 10.0
    top_drivers: List[DriverFeature] = []
    is_rising: bool = False
    has_insights: bool = False
    created_at: Optional[datetime] = None
    metadata: Dict[str, Any] = {}


class ItemDetailResponse(ItemCardResponse):
    insight: Optional[Dict[str, Any]] = None
    all_predictions: List[Dict[str, Any]] = []
