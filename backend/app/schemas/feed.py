from typing import List
from pydantic import BaseModel, ConfigDict
from backend.app.schemas.item import ItemCardResponse


class FeedResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    items: List[ItemCardResponse]
    total: int
    page: int
    limit: int
    pages: int
    has_next: bool
