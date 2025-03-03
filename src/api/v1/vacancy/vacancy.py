from fastapi import (
    APIRouter,
    Depends,
)

from app.controllers import VacancyController
from app.models import (
    User,
    Vacancy,
)
from app.schemas.requests.vacancy import CreateVacancyRequest
from app.schemas.responses.vacancy import VacancyResponse
from core.factory import Factory
from core.fastapi.dependencies.authentication import AuthenticationRequired
from core.fastapi.dependencies.current_user import get_current_user
from src.core.fastapi.dependencies.role_required import RoleRequired


vacancy_router = APIRouter()


@vacancy_router.post(
    "/",
    dependencies=[
        Depends(AuthenticationRequired),
        Depends(RoleRequired(["hr", "admin"])),
    ],
    status_code=201,
)
async def create_vacancy(
    create_vacancy_request: CreateVacancyRequest,
    user: User = Depends(get_current_user),
    vacancy_controller: VacancyController = Depends(Factory().get_vacancy_controller),
) -> VacancyResponse:
    vacancy: Vacancy = await vacancy_controller.create_vacancy(
        title=create_vacancy_request.title,
        description=create_vacancy_request.description,
        requirements=create_vacancy_request.requirements,
        conditions=create_vacancy_request.conditions,
        salary=create_vacancy_request.salary,
        created_by=user,
        employment_type_str=create_vacancy_request.employment_type_str,
    )

    return VacancyResponse(
        uuid=vacancy.uuid,
        title=vacancy.title,
        description=vacancy.description,
        requirements=vacancy.requirements,
        conditions=vacancy.conditions,
        salary=vacancy.salary,
        employment_type=vacancy.employment_type.name,
    )


@vacancy_router.patch(
    "/edit",
    dependencies=[
        Depends(AuthenticationRequired),
        Depends(RoleRequired(["hr", "admin"])),
    ],
    status_code=201,
)
async def edit_vacancy(
    user: User = Depends(get_current_user),
    vacancy_controller: VacancyController = Depends(Factory().get_vacancy_controller),
) -> VacancyResponse:
    return ""
