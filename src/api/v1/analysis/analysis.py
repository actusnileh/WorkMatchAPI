from uuid import UUID

from fastapi import (
    APIRouter,
    Depends,
)

from app.controllers import AnalysisController
from app.schemas.responses.analysis import (
    AnalysisResponse,
    ListAnalysisResponse,
)
from core.factory import Factory


analyse_router = APIRouter()


@analyse_router.get(
    "/specialist/{specialist_uuid}",
    response_model=ListAnalysisResponse,
    summary="Получить все анализы по специалисту",
)
async def get_all_analysis_by_specialist(
    specialist_uuid: UUID,
    analysis_controller: AnalysisController = Depends(Factory().get_analysis_controller),
) -> ListAnalysisResponse:
    """
    Получить все анализы по указанному специалисту по его UUID.
    """
    analysis = await analysis_controller.get_all_by_specialist(specialist_uuid)
    return ListAnalysisResponse(applications=[AnalysisResponse.from_orm(a) for a in analysis])


@analyse_router.get(
    "/vacancy/{vacancy_uuid}",
    response_model=ListAnalysisResponse,
    summary="Получить все анализы по вакансии",
)
async def get_all_analysis_by_vacancy(
    vacancy_uuid: UUID,
    analysis_controller: AnalysisController = Depends(Factory().get_analysis_controller),
) -> ListAnalysisResponse:
    """
    Получить все анализы по указанной вакансии по её UUID.
    """
    analysis = await analysis_controller.get_all_by_vacancy(vacancy_uuid)
    return ListAnalysisResponse(applications=[AnalysisResponse.from_orm(a) for a in analysis])


@analyse_router.get(
    "/{specialist_uuid}/{vacancy_uuid}",
    response_model=AnalysisResponse,
    summary="Получить анализ",
)
async def get_application(
    specialist_uuid: UUID,
    vacancy_uuid: UUID,
    analysis_controller: AnalysisController = Depends(Factory().get_analysis_controller),
) -> AnalysisResponse:
    """
    Возвращает анализ  пользователя на указанную вакансию и специалиста.
    """
    analyse = await analysis_controller.get_by_specialist(specialist_uuid, vacancy_uuid)
    return AnalysisResponse.from_orm(analyse)
