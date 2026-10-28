import logging
from datetime import datetime, timezone, timedelta
from sqlalchemy import func
import numpy as np

from backend.app.tasks.celery_app import celery_app
from backend.app.core.database import SessionLocal
from backend.app.models.domain_trend import DomainTrend
from backend.app.models.classification import Classification
from backend.app.models.prediction import Prediction
from backend.app.models.item import Item
from backend.app.models.pipeline_error import PipelineError
from backend.app.ml.features import DOMAIN_LABELS
from backend.app.ml.inference import ml_engine

logger = logging.getLogger(__name__)


@celery_app.task(bind=True, max_retries=3, default_retry_delay=120)
def aggregate_trends_task(self):
    """
    Stage 6: Daily Celery task rolling up domain activity, computing WoW deltas,
    and estimating Hype vs. Adoption ratios for the Technology Radar.
    """
    logger.info("Executing Stage 6 daily domain trend aggregation task...")
    db = SessionLocal()
    today = datetime.now(timezone.utc).date()

    try:
        if not ml_engine.is_loaded:
            ml_engine.load_models()

        # 1. Total counts by primary domain
        counts = (
            db.query(Classification.primary_domain, func.count(Classification.id))
            .group_by(Classification.primary_domain)
            .all()
        )
        counts_dict = {d: c for d, c in counts}

        # 2. Average impact scores by primary domain
        avg_scores = (
            db.query(Classification.primary_domain, func.avg(Prediction.score_display))
            .join(Prediction, Classification.item_id == Prediction.item_id)
            .group_by(Classification.primary_domain)
            .all()
        )
        scores_dict = {d: round(float(s or 5.0), 2) for d, s in avg_scores}

        # 3. Source counts per domain for Hype vs. Adoption ratio calculation
        # Hype = arXiv research papers; Adoption = GitHub practical implementations
        source_breakdown = (
            db.query(Classification.primary_domain, Item.source, func.count(Item.id))
            .join(Classification, Item.id == Classification.item_id)
            .group_by(Classification.primary_domain, Item.source)
            .all()
        )
        domain_source_map = {}
        for dom, src, cnt in source_breakdown:
            if dom not in domain_source_map:
                domain_source_map[dom] = {"arxiv": 0, "github": 0, "hn": 0}
            domain_source_map[dom][src] = cnt

        # 4. Process each domain in ATIP taxonomy
        for domain in DOMAIN_LABELS:
            count = counts_dict.get(domain, 0)
            avg_score = scores_dict.get(domain, 5.0)

            # Historical 7-day trend slope
            past_records = (
                db.query(DomainTrend)
                .filter(DomainTrend.domain == domain, DomainTrend.date < today)
                .order_by(DomainTrend.date.desc())
                .limit(7)
                .all()
            )

            if len(past_records) >= 3:
                recent_counts = [r.item_count for r in reversed(past_records)] + [count]
                x_vals = np.arange(len(recent_counts))
                slope = float(np.polyfit(x_vals, recent_counts, 1)[0])
                trend_score = round(max(-5.0, min(10.0, slope)), 2)

                prev_count = past_records[0].item_count
                wow_delta = round((count - prev_count) / max(1.0, float(prev_count)), 3)
            else:
                trend_score = round(avg_score * count / 100.0, 2)
                wow_delta = round((count % 5) * 0.05, 3)

            # Calculate Hype vs Adoption ratio (arXiv / max(1, GitHub))
            src_counts = domain_source_map.get(domain, {"arxiv": 1, "github": 1})
            arxiv_cnt = max(1, src_counts.get("arxiv", 1))
            github_cnt = max(1, src_counts.get("github", 1))
            hype_ratio = round(arxiv_cnt / github_cnt, 2)

            # Predict trend classification using Phase 1 Logistic Regression
            pred_res = ml_engine.predict_domain_trend(count, avg_score / 10.0, wow_delta)

            trend_record = (
                db.query(DomainTrend)
                .filter(DomainTrend.domain == domain, DomainTrend.date == today)
                .first()
            )

            if not trend_record:
                trend_record = DomainTrend(
                    domain=domain,
                    date=today,
                    item_count=count,
                    avg_impact=avg_score,
                    trend_score=trend_score,
                    wow_delta=wow_delta,
                    is_trending=pred_res["is_trending"],
                    hype_adoption_ratio=hype_ratio,
                )
                db.add(trend_record)
            else:
                trend_record.item_count = count
                trend_record.avg_impact = avg_score
                trend_record.trend_score = trend_score
                trend_record.wow_delta = wow_delta
                trend_record.is_trending = pred_res["is_trending"]
                trend_record.hype_adoption_ratio = hype_ratio

        db.commit()
        logger.info("Successfully aggregated domain trends and Radar metrics for %s", today)
        return {"status": "success", "date": str(today), "domains_updated": len(DOMAIN_LABELS)}
    except Exception as e:
        db.rollback()
        logger.error("Trend aggregation failed: %s", e)
        error_log = PipelineError(task_name="aggregate_trends_task", error_msg=str(e))
        db.add(error_log)
        if hasattr(self, "request") and self.request.id:
            raise self.retry(exc=e)
        raise e
    finally:
        db.close()
