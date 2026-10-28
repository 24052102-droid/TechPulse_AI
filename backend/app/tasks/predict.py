import logging
from backend.app.tasks.celery_app import celery_app
from backend.app.core.database import SessionLocal
from backend.app.models.item import Item
from backend.app.models.prediction import Prediction
from backend.app.models.pipeline_error import PipelineError
from backend.app.ml.inference import ml_engine

logger = logging.getLogger(__name__)


@celery_app.task(bind=True, max_retries=3, default_retry_delay=60)
def predict_batch_task(self, item_ids: list[str]):
    """
    Stage 4: Supervised XGBoost prediction & TreeSHAP driver extraction.
    """
    if not item_ids:
        return {"status": "skipped", "scored_count": 0}

    logger.info("Executing supervised prediction batch for %d items...", len(item_ids))
    db = SessionLocal()
    scored_count = 0

    try:
        if not ml_engine.is_loaded:
            ml_engine.load_models()

        items = db.query(Item).filter(Item.id.in_(item_ids)).all()
        for item in items:
            existing = db.query(Prediction).filter(Prediction.item_id == item.id).first()
            if existing:
                continue

            item_dict = {
                "title": item.title,
                "description": item.description or "",
                "created_at": item.created_at,
                "metadata": item.metadata_json or {},
            }

            if item.source == "arxiv":
                res = ml_engine.score_paper(item_dict)
                pred_type = "paper_impact"
            elif item.source == "github":
                res = ml_engine.score_repo(item_dict)
                pred_type = "repo_growth"
            else:
                res = ml_engine.score_hn(item_dict)
                pred_type = "hn_velocity"

            pred = Prediction(
                item_id=item.id,
                prediction_type=pred_type,
                score=res["score"],
                score_display=res["score_display"],
                features_used=res["features_used"],
                model_version=res["model_version"],
            )
            db.add(pred)
            scored_count += 1

        db.commit()
        logger.info("Successfully generated %d XGBoost predictions with TreeSHAP drivers", scored_count)
        return {"status": "success", "scored_count": scored_count}
    except Exception as e:
        db.rollback()
        logger.error("Prediction batch task failed: %s", e)
        error_log = PipelineError(task_name="predict_batch_task", error_msg=str(e))
        db.add(error_log)
        if hasattr(self, "request") and self.request.id:
            raise self.retry(exc=e)
        raise e
    finally:
        db.close()
