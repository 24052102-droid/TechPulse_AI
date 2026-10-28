from celery import Celery
from backend.app.core.config import settings

celery_app = Celery(
    "atip_tasks",
    broker=settings.REDIS_URL,
    backend=settings.REDIS_URL,
    include=[
        "backend.app.tasks.ingest",
        "backend.app.tasks.classify",
        "backend.app.tasks.predict",
        "backend.app.tasks.insights",
        "backend.app.tasks.trends",
    ],
)

celery_app.config_from_object("backend.app.tasks.celery_config")
