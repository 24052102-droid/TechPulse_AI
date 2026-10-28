web: uvicorn backend.app.main:app --host 0.0.0.0 --port ${PORT:-8000} --workers 2
worker: celery -A backend.app.tasks.celery_app.celery_app worker --loglevel=info --concurrency=2
beat: celery -A backend.app.tasks.celery_app.celery_app beat --loglevel=info

