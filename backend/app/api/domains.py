from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import datetime, timezone

from backend.app.core.database import get_db
from backend.app.core.redis import cache_client
from backend.app.models.classification import Classification
from backend.app.models.prediction import Prediction
from backend.app.models.domain_trend import DomainTrend
from backend.app.ml.features import DOMAIN_LABELS

router = APIRouter(prefix="/domains", tags=["Domains"])


@router.get("")
def get_domains(db: Session = Depends(get_db)):
    """
    Returns the 10 ATIP technical domains with live item counts,
    average impact scores, and current trend status for the sidebar filter.
    """
    cache_key = "api:domains:summary"
    cached = cache_client.get_json(cache_key)
    if cached:
        return cached

    # Query item counts by domain
    counts = (
        db.query(Classification.primary_domain, func.count(Classification.id))
        .group_by(Classification.primary_domain)
        .all()
    )
    counts_dict = {d: c for d, c in counts}

    # Query average impact by domain
    avg_scores = (
        db.query(Classification.primary_domain, func.avg(Prediction.score_display))
        .join(Prediction, Classification.item_id == Prediction.item_id)
        .group_by(Classification.primary_domain)
        .all()
    )
    scores_dict = {d: round(float(s or 5.0), 1) for d, s in avg_scores}

    # Query latest trend records
    today = datetime.now(timezone.utc).date()
    trends = db.query(DomainTrend).filter(DomainTrend.date == today).all()
    if not trends:
        # Fall back to latest date available
        latest_date = db.query(func.max(DomainTrend.date)).scalar()
        if latest_date:
            trends = db.query(DomainTrend).filter(DomainTrend.date == latest_date).all()
    trend_map = {t.domain: t for t in trends}

    results = []
    for domain in DOMAIN_LABELS:
        count = counts_dict.get(domain, 0)
        avg_impact = scores_dict.get(domain, 5.0)
        trend_rec = trend_map.get(domain)

        results.append({
            "domain": domain,
            "item_count": count,
            "avg_impact": avg_impact,
            "is_trending": bool(trend_rec.is_trending) if trend_rec else False,
            "trend_score": float(trend_rec.trend_score) if trend_rec else 0.0,
            "wow_delta": float(trend_rec.wow_delta) if trend_rec else 0.0,
            "hype_adoption_ratio": float(trend_rec.hype_adoption_ratio) if trend_rec else 1.0,
        })

    # Sort domains by item count descending
    results.sort(key=lambda x: x["item_count"], reverse=True)

    cache_client.set_json(cache_key, results, ex=120)
    return results
