from fastapi import (
    APIRouter,
    Depends,
)

from core.fastapi.dependencies.authentication import AuthenticationRequired
from app.controllers import VacancyController
from core.factory import Factory
from app.models import User
from core.fastapi.dependencies.current_user import get_current_user
from app.schemas.requests.vacancy import CreateVacancyRequest
from app.schemas.responses.vacancy import VacancyResponse


vacancy_router = APIRouter()


@vacancy_router.post(
    "/", dependencies=[Depends(AuthenticationRequired)], status_code=201
)
async def create_vacancy(
    create_vacancy_request: CreateVacancyRequest,
    user: User = Depends(get_current_user),
    vacancy_controller: VacancyController = Depends(Factory().get_vacancy_controller),
) -> VacancyResponse:
    vacancy = await vacancy_controller.create_vacancy(
        title=create_vacancy_request.title,
        description=create_vacancy_request.description,
        requirements=create_vacancy_request.requirements,
        conditions=create_vacancy_request.conditions,
        created_by=user[0],
        employment_type_str=create_vacancy_request.employment_type_str,
    )

    return VacancyResponse(
        title=vacancy.title,
        description=vacancy.description,
        requirements=vacancy.requirements,
        conditions=vacancy.conditions,
        employment_type=vacancy.employment_type.name,
    )
