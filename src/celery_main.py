from celery import Celery

from src.core.config import settings

celery_app = Celery('celery_main', broker=settings.REDIS_URL, include=["src.tasks", ])
celery_app.conf.update(
    task_serializer='json',
    accept_content=['json'],  # Ignore other content
    result_serializer='json',
    timezone='Europe/Moscow',
    enable_utc=True,
)


