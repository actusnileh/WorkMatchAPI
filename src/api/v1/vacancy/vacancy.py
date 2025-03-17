from fastapi import (
    APIRouter,
    Depends,
)

from app.controllers import VacancyController
from app.models import (
    User,
    Vacancy,
)
from app.schemas.requests.vacancy import (
    CreateVacancyRequest,
    EditVacancyRequest,
)
from app.schemas.responses.vacancy import VacancyResponse
from core.factory import Factory
from core.fastapi.dependencies.authentication import AuthenticationRequired
from core.fastapi.dependencies.current_user import get_current_user
from core.fastapi.dependencies.role_required import RoleRequired


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

    return VacancyResponse.from_orm(vacancy)


@vacancy_router.patch(
    "/edit/{vacancy_uuid}",
    dependencies=[
        Depends(AuthenticationRequired),
        Depends(RoleRequired(["hr", "admin"])),
    ],
    status_code=200,
)
async def edit_vacancy(
    vacancy_uuid: str,
    edit_vacancy_request: EditVacancyRequest,
    user: User = Depends(get_current_user),
    vacancy_controller: VacancyController = Depends(Factory().get_vacancy_controller),
) -> VacancyResponse:
    vacancy: Vacancy = await vacancy_controller.update_by_uuid(
        user=user,
        uuid=vacancy_uuid,
        attrs=edit_vacancy_request.model_dump(exclude_unset=True),
    )

    return VacancyResponse.from_orm(vacancy)
