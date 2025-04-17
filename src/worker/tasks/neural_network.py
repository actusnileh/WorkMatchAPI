from typing import Any
from src.worker import celery_app
import httpx

from core.config import config

client = httpx.Client(
    base_url=config.NEURAL_SERVICE_URL,
    timeout=httpx.Timeout(10.0, connect=5.0),
    limits=httpx.Limits(max_connections=10, max_keepalive_connections=5),
)


@celery_app.task(
    bind=True,
    autoretry_for=(httpx.RequestError,),
    retry_backoff=True,
    retry_backoff_max=60,
    retry_jitter=True,
    max_retries=5,
)
def apply_neural_network(self, vacancy, specialist) -> dict[str, Any]:
    print(vacancy, specialist)
    # resp = client.post("/", json=vacancy)
    # resp.raise_for_status()
    # return resp.json()
