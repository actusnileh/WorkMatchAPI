from fastapi import APIRouter

from app.schemas.extras.health import Health
from core.config import config


health_router = APIRouter()


@health_router.get(
    "/",
    response_model=Health,
    summary="Проверка состояния системы",
)
async def health() -> Health:
    """
    Проверяет состояние системы и возвращает текущую версию приложения
    вместе со статусом.
    """
    return Health(version=config.RELEASE_VERSION, status="Healthy")
