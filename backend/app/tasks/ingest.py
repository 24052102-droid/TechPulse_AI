import logging
from datetime import datetime, timezone
from backend.app.tasks.celery_app import celery_app
from backend.app.core.database import SessionLocal
from backend.app.models.item import Item
from backend.app.models.pipeline_error import PipelineError
from backend.app.services.arxiv_service import ArxivService
from backend.app.services.github_service import GitHubService
from backend.app.services.hn_service import HNService

logger = logging.getLogger(__name__)


def _insert_items_safely(raw_items: list[dict], source_name: str) -> list[str]:
    """
    Safely inserts newly fetched items into the database with deduplication on source_id.
    Returns list of newly created item UUIDs.
    """
    db = SessionLocal()
    new_item_ids = []
    try:
        for r in raw_items:
            source_id = str(r["source_id"])
            existing = db.query(Item).filter(Item.source_id == source_id).first()
            if existing:
                continue

            item = Item(
                source=r["source"],
                source_id=source_id,
                title=r["title"],
                description=r["description"],
                url=r["url"],
                metadata_json=r.get("metadata", {}),
                created_at=r.get("created_at") or datetime.now(timezone.utc),
            )
            db.add(item)
            db.flush()  # Populates item.id
            new_item_ids.append(item.id)

        db.commit()
        logger.info("[%s] Inserted %d new items (skipped %d existing)", 
                    source_name, len(new_item_ids), len(raw_items) - len(new_item_ids))
    except Exception as e:
        db.rollback()
        logger.error("[%s] Database insertion failed: %s", source_name, e)
        error_log = PipelineError(task_name=f"ingest_{source_name}", error_msg=str(e))
        db.add(error_log)
        db.commit()
        raise e
    finally:
        db.close()

    return new_item_ids


@celery_app.task(bind=True, max_retries=3, default_retry_delay=120)
def ingest_arxiv_task(self, max_results: int = 30):
    """Celery task to ingest new arXiv papers across target CS categories."""
    logger.info("Executing scheduled arXiv ingestion task (max_results=%d)...", max_results)
    try:
        service = ArxivService()
        raw_papers = service.fetch_recent_papers(max_results=max_results)
        new_ids = _insert_items_safely(raw_papers, "arxiv")
        return {"status": "success", "source": "arxiv", "new_item_ids": new_ids, "count": len(new_ids)}
    except Exception as e:
        logger.error("arXiv ingestion failed: %s", e)
        raise self.retry(exc=e)


@celery_app.task(bind=True, max_retries=3, default_retry_delay=120)
def ingest_github_task(self, max_results: int = 30):
    """Celery task to ingest trending GitHub repositories."""
    logger.info("Executing scheduled GitHub ingestion task (max_results=%d)...", max_results)
    try:
        service = GitHubService()
        raw_repos = service.fetch_trending_repos(max_results=max_results)
        new_ids = _insert_items_safely(raw_repos, "github")
        return {"status": "success", "source": "github", "new_item_ids": new_ids, "count": len(new_ids)}
    except Exception as e:
        logger.error("GitHub ingestion failed: %s", e)
        raise self.retry(exc=e)


@celery_app.task(bind=True, max_retries=3, default_retry_delay=120)
def ingest_hn_task(self, max_results: int = 30):
    """Celery task to ingest Hacker News stories."""
    logger.info("Executing periodic Hacker News ingestion task (max_results=%d)...", max_results)
    try:
        service = HNService()
        raw_stories = service.fetch_top_tech_stories(max_results=max_results)
        new_ids = _insert_items_safely(raw_stories, "hn")
        return {"status": "success", "source": "hn", "new_item_ids": new_ids, "count": len(new_ids)}
    except Exception as e:
        logger.error("HN ingestion failed: %s", e)
        raise self.retry(exc=e)
