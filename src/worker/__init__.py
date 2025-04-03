import time

from celery import Celery

from core.config import config


celery_app = Celery(
    "worker",
    backend=config.CELERY_BACKEND_URL,
    broker=config.CELERY_BROKER_URL,
)

celery_app.conf.task_routes = {"src.celery_app.add": "test-queue"}
celery_app.conf.update(task_track_started=True)


@celery_app.task
def add(x, y):
    time.sleep(10)
    return x + y
