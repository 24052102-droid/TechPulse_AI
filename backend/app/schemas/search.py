from typing import List
from pydantic import BaseModel, ConfigDict
from backend.app.schemas.item import ItemCardResponse


class SearchResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    query: str
    total: int
    results: List[ItemCardResponse]
    took_ms: float
