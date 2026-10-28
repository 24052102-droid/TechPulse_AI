import logging
from backend.app.tasks.celery_app import celery_app
from backend.app.core.database import SessionLocal
from backend.app.models.item import Item
from backend.app.models.classification import Classification
from backend.app.models.insight import Insight
from backend.app.models.pipeline_error import PipelineError
from backend.app.services.llm_service import LLMService

logger = logging.getLogger(__name__)


def _generate_and_save_insight(db, item: Item, llm_service: LLMService) -> bool:
    """Helper to generate and save insight for a single item."""
    cls = db.query(Classification).filter(Classification.item_id == item.id).first()
    primary_domain = cls.primary_domain if cls else "General Machine Learning"

    ins_data = llm_service.generate_insight(
        source_id=item.source_id,
        title=item.title,
        description=item.description or "",
        source=item.source,
        primary_domain=primary_domain,
    )

    existing = db.query(Insight).filter(Insight.item_id == item.id).first()
    if not existing:
        ins = Insight(
            item_id=item.id,
            summary=ins_data["summary"],
            key_takeaways=ins_data["key_takeaways"],
            why_it_matters=ins_data["why_it_matters"],
            technical_depth=ins_data.get("technical_depth", "intermediate"),
            estimated_read_time=ins_data.get("estimated_read_time", 5),
            related_topics=ins_data.get("related_topics", []),
            llm_model=ins_data.get("llm_model", "claude-3-5-sonnet"),
        )
        db.add(ins)
        return True
    return False


@celery_app.task(bind=True, max_retries=2, default_retry_delay=60)
def generate_insights_batch_task(self, item_ids: list[str]):
    """
    Stage 5: Batch LLM insight synthesis with Redis cache guardrail (NFR-06).
    """
    if not item_ids:
        return {"status": "skipped", "generated_count": 0}

    logger.info("Executing LLM insight generation batch for %d items...", len(item_ids))
    db = SessionLocal()
    generated_count = 0
    llm_service = LLMService()

    try:
        items = db.query(Item).filter(Item.id.in_(item_ids)).all()
        for item in items:
            existing = db.query(Insight).filter(Insight.item_id == item.id).first()
            if existing:
                continue

            saved = _generate_and_save_insight(db, item, llm_service)
            if saved:
                generated_count += 1

        db.commit()
        logger.info("Successfully generated and cached %d AI insights", generated_count)
        return {"status": "success", "generated_count": generated_count}
    except Exception as e:
        db.rollback()
        logger.error("Insight batch generation failed: %s", e)
        error_log = PipelineError(task_name="generate_insights_batch_task", error_msg=str(e))
        db.add(error_log)
        if hasattr(self, "request") and self.request.id:
            raise self.retry(exc=e)
        raise e
    finally:
        db.close()


@celery_app.task(bind=True, max_retries=2, default_retry_delay=30)
def generate_single_insight(self, item_id: str):
    """
    On-demand asynchronous insight generator for the lazy-loading API endpoint (GET /api/item/{id}/insights).
    """
    db = SessionLocal()
    llm_service = LLMService()
    try:
        item = db.query(Item).filter(Item.id == item_id).first()
        if not item:
            return {"status": "error", "message": "Item not found"}

        existing = db.query(Insight).filter(Insight.item_id == item_id).first()
        if existing:
            return {"status": "ready", "item_id": item_id}

        _generate_and_save_insight(db, item, llm_service)
        db.commit()
        return {"status": "ready", "item_id": item_id}
    except Exception as e:
        db.rollback()
        logger.error("Single insight generation failed for item %s: %s", item_id, e)
        error_log = PipelineError(task_name="generate_single_insight", item_id=item_id, error_msg=str(e))
        db.add(error_log)
        if hasattr(self, "request") and self.request.id:
            raise self.retry(exc=e)
        raise e
    finally:
        db.close()
