from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, ConfigDict


class InsightResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    item_id: str
    summary: str
    key_takeaways: List[str]
    why_it_matters: str
    technical_depth: str
    estimated_read_time: int
    related_topics: List[str]
    llm_model: str
    generated_at: datetime


class InsightStatusResponse(BaseModel):
    status: str  # "ready" | "processing" | "failed"
    item_id: str
    insight: Optional[InsightResponse] = None
