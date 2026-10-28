from backend.app.tasks.celery_app import celery_app
from backend.app.tasks.ingest import ingest_arxiv_task, ingest_github_task, ingest_hn_task
from backend.app.tasks.enrich import enrich_arxiv_batch_task
from backend.app.tasks.classify import classify_batch_task
from backend.app.tasks.predict import predict_batch_task
from backend.app.tasks.insights import generate_insights_batch_task, generate_single_insight
from backend.app.tasks.trends import aggregate_trends_task

__all__ = [
    "celery_app",
    "ingest_arxiv_task",
    "ingest_github_task",
    "ingest_hn_task",
    "enrich_arxiv_batch_task",
    "classify_batch_task",
    "predict_batch_task",
    "generate_insights_batch_task",
    "generate_single_insight",
    "aggregate_trends_task",
]
