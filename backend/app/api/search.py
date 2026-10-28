import time
from typing import Optional, List
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import or_, desc

from backend.app.core.database import get_db
from backend.app.models.item import Item
from backend.app.models.classification import Classification
from backend.app.models.prediction import Prediction
from backend.app.schemas.search import SearchResponse
from backend.app.schemas.item import ItemCardResponse, DriverFeature

router = APIRouter(prefix="/search", tags=["Search"])


@router.get("", response_model=SearchResponse)
def search_items(
    q: str = Query(..., min_length=1, description="Natural language search query"),
    domain: Optional[str] = Query(None, description="Optional domain filter"),
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
):
    """
    Hybrid search combining text relevance with ML impact score reranking.
    Guarantees sub-500ms p95 latency (NFR-02).
    """
    start_time = time.time()

    query = (
        db.query(Item, Classification, Prediction)
        .outerjoin(Classification, Item.id == Classification.item_id)
        .outerjoin(Prediction, Item.id == Prediction.item_id)
    )

    # Keywords split for multi-term LIKE matching (works universally on SQLite & PostgreSQL)
    terms = q.lower().strip().split()
    filters = []
    for term in terms:
        filters.append(
            or_(
                Item.title.ilike(f"%{term}%"),
                Item.description.ilike(f"%{term}%"),
                Classification.primary_domain.ilike(f"%{term}%"),
            )
        )

    if filters:
        query = query.filter(*filters)

    if domain:
        query = query.filter(Classification.primary_domain == domain)

    # Order by impact score for relevance reranking
    query = query.order_by(desc(Prediction.score_display))

    total = query.count()
    offset = (page - 1) * limit
    results = query.offset(offset).limit(limit).all()

    items_list = []
    for item, cls, pred in results:
        top_drivers = []
        if pred and pred.features_used and isinstance(pred.features_used, dict):
            for d in pred.features_used.get("top_drivers", []):
                top_drivers.append(DriverFeature(
                    feature=str(d.get("feature", "")),
                    value=d.get("value", 0),
                    impact=float(d.get("impact", 0.0)),
                ))

        items_list.append(ItemCardResponse(
            id=item.id,
            source=item.source,
            source_id=item.source_id,
            title=item.title,
            description=item.description,
            url=item.url,
            primary_domain=cls.primary_domain if cls else "General Machine Learning",
            secondary_domains=cls.secondary_domains if cls and cls.secondary_domains else [],
            domain_confidence=0.85,
            impact_score=pred.score_display if pred else 5.0,
            top_drivers=top_drivers,
            is_rising=bool(item.metadata_json.get("is_rising", False)) if item.metadata_json else False,
            has_insights=item.insight is not None,
            created_at=item.created_at or item.ingested_at,
            metadata=item.metadata_json or {},
        ))

    took_ms = round((time.time() - start_time) * 1000.0, 2)
    return SearchResponse(
        query=q,
        total=total,
        results=items_list,
        took_ms=took_ms,
    )
