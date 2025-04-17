import time

from celery import Celery

from core.config import config

celery_app = Celery(
    "worker",
    backend=config.REDIS_URL,
    broker=config.CELERY_BROKER_URL,
    include=["src.worker.tasks"],
)

celery_app.conf.update(task_track_started=True)
