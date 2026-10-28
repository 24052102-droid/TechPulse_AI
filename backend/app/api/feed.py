from typing import Optional, List
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import desc, func

from backend.app.core.database import get_db
from backend.app.core.redis import cache_client
from backend.app.core.config import settings
from backend.app.models.item import Item
from backend.app.models.classification import Classification
from backend.app.models.prediction import Prediction
from backend.app.models.insight import Insight
from backend.app.schemas.feed import FeedResponse
from backend.app.schemas.item import ItemCardResponse, DriverFeature

router = APIRouter(prefix="/feed", tags=["Feed"])


@router.get("", response_model=FeedResponse)
def get_feed(
    domain: Optional[str] = Query(None, description="Comma-separated domain filters"),
    source: Optional[str] = Query(None, description="Filter by source: arxiv, github, hn"),
    sort: str = Query("impact_score", description="Sort by: impact_score, recent, trending"),
    page: int = Query(1, ge=1, description="Page number"),
    limit: int = Query(20, ge=1, le=100, description="Items per page"),
    db: Session = Depends(get_db),
):
    """
    Main intelligence feed returning items with classifications and impact predictions.
    Cached in Redis for 5 minutes (TTL: 300s).
    """
    # Parse domain filter list
    domains_list = [d.strip() for d in domain.split(",") if d.strip()] if domain else []
    domains_key = ",".join(sorted(domains_list)) if domains_list else "all"
    source_key = source.lower() if source else "all"

    cache_key = f"api:feed:{sort}:{domains_key}:{source_key}:p{page}:l{limit}"
    cached_data = cache_client.get_json(cache_key)
    if cached_data:
        return cached_data

    # Query with left joins
    query = (
        db.query(Item, Classification, Prediction, Insight)
        .outerjoin(Classification, Item.id == Classification.item_id)
        .outerjoin(Prediction, Item.id == Prediction.item_id)
        .outerjoin(Insight, Item.id == Insight.item_id)
    )

    # Apply filters
    if source and source.lower() != "all":
        query = query.filter(Item.source == source.lower())

    if domains_list:
        query = query.filter(Classification.primary_domain.in_(domains_list))

    # Apply sorting
    if sort == "recent":
        query = query.order_by(desc(func.coalesce(Item.created_at, Item.ingested_at)))
    elif sort == "trending":
        # Sort by impact score combined with recency
        query = query.order_by(desc(Prediction.score_display), desc(Item.ingested_at))
    else:  # impact_score (default)
        query = query.order_by(desc(Prediction.score_display))

    total = query.count()
    offset = (page - 1) * limit
    results = query.offset(offset).limit(limit).all()

    items_list = []
    for item, cls, pred, ins in results:
        # Extract top drivers safely from prediction features_used
        top_drivers = []
        if pred and pred.features_used and isinstance(pred.features_used, dict):
            raw_drivers = pred.features_used.get("top_drivers", [])
            for d in raw_drivers:
                top_drivers.append(DriverFeature(
                    feature=str(d.get("feature", "")),
                    value=d.get("value", 0),
                    impact=float(d.get("impact", 0.0)),
                ))

        card = ItemCardResponse(
            id=item.id,
            source=item.source,
            source_id=item.source_id,
            title=item.title,
            description=item.description,
            url=item.url,
            primary_domain=cls.primary_domain if cls else "General Machine Learning",
            secondary_domains=cls.secondary_domains if cls and cls.secondary_domains else [],
            domain_confidence=cls.confidence_scores.get(cls.primary_domain, 0.8) if cls and cls.confidence_scores else 0.8,
            impact_score=pred.score_display if pred else 5.0,
            top_drivers=top_drivers,
            is_rising=bool(item.metadata_json.get("is_rising", False)) if item.metadata_json else False,
            has_insights=ins is not None,
            created_at=item.created_at or item.ingested_at,
            metadata=item.metadata_json or {},
        )
        items_list.append(card)

    pages = max(1, (total + limit - 1) // limit)
    response_data = {
        "items": [item.model_dump(mode="json") for item in items_list],
        "total": total,
        "page": page,
        "limit": limit,
        "pages": pages,
        "has_next": page < pages,
    }

    # Cache response in Redis
    cache_client.set_json(cache_key, response_data, ex=settings.REDIS_FEED_CACHE_TTL)
    return response_data
