from celery import Celery
from src.config import settings

app = Celery(
    "cv-simulator",
    broker=settings.rabbitmq_url,
    backend=settings.redis_url,
    include=["src.tasks"],
)

app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
    task_track_started=True,
)
