from uuid import UUID

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
from app.schemas.responses.vacancy import (
    ListPaginatedVacancyResponse,
    ListVacancyResponse,
    VacancyResponse,
)
from core.factory import Factory
from core.fastapi.dependencies.authentication import AuthenticationRequired
from core.fastapi.dependencies.current_user import get_current_user
from core.fastapi.dependencies.role_required import RoleRequired


vacancy_router = APIRouter()


@vacancy_router.post(
    "/",
    summary="Создать новую вакансию",
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
    """
    Создает новую вакансию для HR или администратора.
    """
    vacancy: Vacancy = await vacancy_controller.create_vacancy(
        title=create_vacancy_request.title,
        description=create_vacancy_request.description,
        requirements=create_vacancy_request.requirements,
        conditions=create_vacancy_request.conditions,
        salary=create_vacancy_request.salary,
        created_by=user,
        employment_type_str=create_vacancy_request.employment_type_str,
    )
    return VacancyResponse.from_orm(vacancy[0])


@vacancy_router.get(
    "/",
    summary="Получить список вакансий",
    status_code=200,
)
async def get_vacancies(
    skip: int = 0,
    limit: int = 50,
    vacancy_controller: VacancyController = Depends(Factory().get_vacancy_controller),
) -> ListPaginatedVacancyResponse:
    """
    Возвращает список всех вакансий с пагинацией.
    """
    vacancies, total_count = await vacancy_controller.get_all(skip, limit)
    return ListPaginatedVacancyResponse(
        Vacancies=[VacancyResponse.from_orm(v) for v in vacancies],
        Count=total_count,
    )


@vacancy_router.get(
    "/search",
    summary="Найти вакансии",
    status_code=200,
)
async def search_vacancies(
    query: str,
    skip: int = 0,
    limit: int = 10,
    vacancy_controller: VacancyController = Depends(Factory().get_vacancy_controller),
) -> ListVacancyResponse:
    """
    Выполняет поиск вакансий по ключевым словам.
    """
    vacancies = await vacancy_controller.search_vacancies(query=query, skip=skip, limit=limit)
    return ListVacancyResponse(
        Vacancies=[VacancyResponse.from_orm(v) for v in vacancies],
    )


@vacancy_router.get(
    "/get_my",
    summary="Получить мои вакансии",
    dependencies=[Depends(AuthenticationRequired)],
    status_code=200,
)
async def get_my_vacancies(
    user: User = Depends(get_current_user),
    vacancy_controller: VacancyController = Depends(Factory().get_vacancy_controller),
) -> ListVacancyResponse:
    """
    Возвращает список вакансий, созданных текущим пользователем.
    """
    vacancies = await vacancy_controller.get_by_user(user)
    return ListVacancyResponse(
        Vacancies=[VacancyResponse.from_orm(v) for v in vacancies],
    )


@vacancy_router.get(
    "/{vacancy_uuid}",
    summary="Получить вакансию по UUID",
    status_code=200,
)
async def get_vacancy(
    vacancy_uuid: UUID,
    vacancy_controller: VacancyController = Depends(Factory().get_vacancy_controller),
) -> VacancyResponse:
    """
    Возвращает информацию о вакансии по ее UUID.
    """
    vacancy = await vacancy_controller.get_by_uuid(uuid=vacancy_uuid, join_={"employment_types"})
    return VacancyResponse.from_orm(vacancy[0])


@vacancy_router.patch(
    "/edit/{vacancy_uuid}",
    summary="Редактировать вакансию",
    dependencies=[
        Depends(AuthenticationRequired),
        Depends(RoleRequired(["hr", "admin"])),
    ],
    status_code=200,
)
async def edit_vacancy(
    vacancy_uuid: UUID,
    edit_vacancy_request: EditVacancyRequest,
    user: User = Depends(get_current_user),
    vacancy_controller: VacancyController = Depends(Factory().get_vacancy_controller),
) -> VacancyResponse:
    """
    Редактирует вакансию, указанную по UUID.
    """
    vacancy: Vacancy = await vacancy_controller.update_by_uuid(
        user=user,
        uuid=vacancy_uuid,
        attrs=edit_vacancy_request.model_dump(exclude_unset=True),
    )
    return VacancyResponse.from_orm(vacancy)


@vacancy_router.delete(
    "/{vacancy_uuid}",
    summary="Удалить вакансию",
    dependencies=[
        Depends(AuthenticationRequired),
        Depends(RoleRequired(["hr", "admin"])),
    ],
    status_code=204,
)
async def delete_vacancy(
    vacancy_uuid: UUID,
    user: User = Depends(get_current_user),
    vacancy_controller: VacancyController = Depends(Factory().get_vacancy_controller),
) -> None:
    """
    Удаляет вакансию, указанную по UUID.
    """
    await vacancy_controller.delete_by_uuid(user, vacancy_uuid)
