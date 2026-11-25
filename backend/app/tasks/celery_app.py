from celery import Celery
from celery.schedules import crontab

from app.core.config import settings


celery_app = Celery(
    "genannotate",
    broker=settings.CELERY_BROKER_URL,
    backend=settings.CELERY_RESULT_BACKEND,
)

celery_app.conf.update(
    include=[
        "app.tasks.import_tasks",
        "app.tasks.export_tasks",
        "app.tasks.dashboard_tasks",
    ],
    beat_schedule={
        "aggregate-dashboard-metrics": {
            "task": "aggregate_dashboard_metrics",
            "schedule": crontab(hour=2, minute=0),
        },
    },
    task_track_started=True,
    task_serializer="json",
    result_serializer="json",
    accept_content=["json"],
    timezone="UTC",
    enable_utc=True,
)