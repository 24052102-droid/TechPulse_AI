from celery.schedules import crontab

# Celery Configuration
task_serializer = "json"
accept_content = ["json"]
result_serializer = "json"
timezone = "Asia/Kolkata"
enable_utc = True
task_track_started = True
task_time_limit = 30 * 60  # 30 minutes

# Celery Beat Daily Schedule
beat_schedule = {
    # 00:30 IST: Ingest daily arXiv papers across 7 CS categories
    "ingest-daily-arxiv": {
        "task": "backend.app.tasks.ingest.ingest_arxiv_task",
        "schedule": crontab(hour=0, minute=30),
    },
    # 01:00 IST: Ingest trending GitHub ML repositories
    "ingest-daily-github": {
        "task": "backend.app.tasks.ingest.ingest_github_task",
        "schedule": crontab(hour=1, minute=0),
    },
    # Every 6 hours: Ingest active Hacker News ML discussions
    "ingest-periodic-hn": {
        "task": "backend.app.tasks.ingest.ingest_hn_task",
        "schedule": crontab(minute=0, hour="*/6"),
    },
    # 02:00 IST: Daily domain trend and technology radar rollups
    "aggregate-daily-trends": {
        "task": "backend.app.tasks.trends.aggregate_trends_task",
        "schedule": crontab(hour=2, minute=0),
    },
}
