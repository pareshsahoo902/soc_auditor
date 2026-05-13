from celery import Celery
from shared.configs.settings import settings

celery_app = Celery(
    "governance_worker",
    broker=settings.REDIS_URL,
    backend=settings.REDIS_URL,
    include=["apps.worker.tasks"]
)

celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
    task_routes={
        "apps.worker.tasks.process_ingestion": {"queue": "ingestion_queue"},
        "apps.worker.tasks.process_extraction": {"queue": "extraction_queue"},
        "apps.worker.tasks.process_governance": {"queue": "governance_queue"},
        "apps.worker.tasks.process_reporting": {"queue": "reporting_queue"},
    }
)
