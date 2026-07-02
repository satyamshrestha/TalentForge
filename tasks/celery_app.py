from celery import Celery
celery = Celery(
    "TalentForge",
    broker="redis://redis:6379/0",
    backend="redis://redis:6379/0",
    include=["tasks.resume_tasks"]
)