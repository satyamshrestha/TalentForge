from celery import Celery

from utils.config import settings

celery = Celery(
    "TalentForge",
    broker=settings.REDIS_URL,
    backend=settings.REDIS_URL,
    include=["tasks.resume_tasks"]
)