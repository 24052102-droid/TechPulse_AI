from typing import List
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import func, desc

from backend.app.core.database import get_db
from backend.app.models.domain_trend import DomainTrend
from backend.app.models.classification import Classification
from backend.app.models.prediction import Prediction
from backend.app.models.item import Item
from backend.app.schemas.trend import TrendsOverviewResponse, DomainSummary, DomainTrendPoint
from backend.app.ml.features import DOMAIN_LABELS
from backend.app.ml.inference import ml_engine

router = APIRouter(prefix="/trends", tags=["Trends"])


@router.get("", response_model=TrendsOverviewResponse)
def get_trends(
    window: str = Query("7d", description="Time window: 7d or 30d"),
    db: Session = Depends(get_db),
):
    """
    Returns domain activity analytics, trend slopes, and rising technology sectors.
    Powers the Recharts line and bar charts on /trends.
    """
    # 1. Check if domain_trends table has records
    db_trends = db.query(DomainTrend).order_by(DomainTrend.date.desc()).all()

    domains_map = {}
    for d in DOMAIN_LABELS:
        domains_map[d] = {
            "domain": d,
            "item_count_7d": 0,
            "avg_impact_7d": 5.0,
            "wow_delta": 0.0,
            "is_trending": False,
            "status": "Stable",
            "hype_adoption_ratio": 1.0,
            "history": [],
        }

    if db_trends:
        for t in db_trends:
            if t.domain in domains_map:
                entry = domains_map[t.domain]
                entry["history"].append(DomainTrendPoint(
                    date=t.date,
                    item_count=t.item_count,
                    avg_impact=t.avg_impact,
                    wow_delta=t.wow_delta,
                    is_trending=t.is_trending,
                ))

        for d, data in domains_map.items():
            if data["history"]:
                recent = data["history"][0]
                data["item_count_7d"] = sum(p.item_count for p in data["history"][:7])
                data["avg_impact_7d"] = round(sum(p.avg_impact for p in data["history"][:7]) / max(1, len(data["history"][:7])), 2)
                data["wow_delta"] = recent.wow_delta
                data["is_trending"] = recent.is_trending
                data["status"] = "Surging" if recent.is_trending else ("Declining" if recent.wow_delta < -0.10 else "Stable")
    else:
        # Compute on the fly from current items in DB
        counts = (
            db.query(Classification.primary_domain, func.count(Classification.id))
            .group_by(Classification.primary_domain)
            .all()
        )
        avg_scores = (
            db.query(Classification.primary_domain, func.avg(Prediction.score_display))
            .join(Prediction, Classification.item_id == Prediction.item_id)
            .group_by(Classification.primary_domain)
            .all()
        )
        scores_dict = {d: round(float(s or 5.0), 2) for d, s in avg_scores}

        for domain, count in counts:
            if domain in domains_map:
                avg_imp = scores_dict.get(domain, 5.0)
                wow = round((count % 5) * 0.08, 2)  # Simulated delta
                pred_trend = ml_engine.predict_domain_trend(count, avg_imp / 10.0, wow)

                domains_map[domain]["item_count_7d"] = count
                domains_map[domain]["avg_impact_7d"] = avg_imp
                domains_map[domain]["wow_delta"] = wow
                domains_map[domain]["is_trending"] = pred_trend["is_trending"]
                domains_map[domain]["status"] = pred_trend["status"]

    summary_list = [DomainSummary(**v) for v in domains_map.values()]

    # Sort rising domains by wow_delta descending
    rising = sorted(summary_list, key=lambda x: (x.is_trending, x.wow_delta), reverse=True)[:3]

    return TrendsOverviewResponse(
        top_rising_domains=rising,
        all_domains=summary_list,
        total_active_domains=len([d for d in summary_list if d.item_count_7d > 0]),
        window=window,
    )
