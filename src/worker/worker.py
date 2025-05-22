import asyncio

import httpx
from celery import Celery

from app.models import AnalysisResult
from app.repositories.analysis import AnalysisRepository
from core.config import config
from core.database import standalone_session
from core.database.session import async_session_factory


celery_app = Celery(
    "worker",
    backend=config.REDIS_URL,
    broker=config.CELERY_BROKER_URL,
)

celery_app.conf.update(task_track_started=True)

client = httpx.AsyncClient(
    base_url=config.NEURAL_SERVICE_URL,
    timeout=httpx.Timeout(230.0, connect=5.0),
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
def apply_neural_network(self, vacancy, specialist) -> dict:
    result = asyncio.run(async_apply_neural_network(vacancy, specialist))
    return result


async def async_apply_neural_network(vacancy, specialist):
    resp = await client.post(
        url="/vacancy_match",
        json={
            "job": vacancy,
            "resume": specialist,
        },
    )
    resp.raise_for_status()
    result = resp.json()

    await create_analysis_result(vacancy, specialist, result)
    return result


@standalone_session
async def create_analysis_result(vacancy, specialist, result):
    await AnalysisRepository(model=AnalysisResult, db_session=async_session_factory()).create(
        {
            "vacancy_id": vacancy["uuid"],
            "specialist_id": specialist["uuid"],
            "match_percentage": result["match_percentage"],
            "mismatches": result["didnt_match"],
        },
    )
