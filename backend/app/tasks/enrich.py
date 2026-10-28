import logging
from backend.app.tasks.celery_app import celery_app
from backend.app.core.database import SessionLocal
from backend.app.models.item import Item
from backend.app.models.pipeline_error import PipelineError
from backend.app.services.semantic_scholar_service import SemanticScholarService

logger = logging.getLogger(__name__)


@celery_app.task(bind=True, max_retries=3, default_retry_delay=60)
def enrich_arxiv_batch_task(self, item_ids: list[str]):
    """
    Stage 2: Enriches arXiv papers with citations, author h-index,
    and cross-referenced code repositories.
    """
    if not item_ids:
        return {"status": "skipped", "enriched_count": 0}

    logger.info("Executing Semantic Scholar enrichment for %d items...", len(item_ids))
    db = SessionLocal()
    enriched_count = 0
    try:
        items = db.query(Item).filter(Item.id.in_(item_ids), Item.source == "arxiv").all()
        if not items:
            return {"status": "success", "enriched_count": 0}

        arxiv_map = {item.source_id: item for item in items}
        service = SemanticScholarService()
        metrics = service.batch_enrich_papers(list(arxiv_map.keys()))

        for source_id, item in arxiv_map.items():
            meta = dict(item.metadata_json or {})
            s2_data = metrics.get(source_id, {})
            meta["citation_count"] = s2_data.get("citation_count", meta.get("citation_count", 0))
            meta["influential_citation_count"] = s2_data.get("influential_citation_count", meta.get("influential_citation_count", 0))
            meta["max_h_index"] = s2_data.get("max_h_index", meta.get("max_h_index", 0))
            
            item.metadata_json = meta
            enriched_count += 1

        db.commit()
        logger.info("Successfully enriched %d arXiv papers with academic metrics", enriched_count)
        return {"status": "success", "enriched_count": enriched_count}
    except Exception as e:
        db.rollback()
        logger.error("Enrichment task failed: %s", e)
        error_log = PipelineError(task_name="enrich_arxiv_batch_task", error_msg=str(e))
        db.add(error_log)
        if hasattr(self, "request") and self.request.id:
            raise self.retry(exc=e)
        raise e
    finally:
        db.close()
