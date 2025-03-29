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
    ListVacancyResponse,
    VacancyResponse,
)
from core.cache import Cache
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
    await Cache.remove_by_prefix("vacancy:all")
    await Cache.remove_by_prefix(f"vacancy:me:{user.o_id}")
    await Cache.remove_by_prefix(f"vacancy:uuid:{vacancy[0].uuid}")
    return VacancyResponse.from_orm(vacancy[0])


@vacancy_router.get(
    "/",
    status_code=200,
)
@Cache.cached(prefix="vacancy:all", ttl=60)
async def get_vacancies(
    skip: int = 0,
    limit: int = 50,
    vacancy_controller: VacancyController = Depends(Factory().get_vacancy_controller),
) -> ListVacancyResponse:
    vacancies = await vacancy_controller.get_all(skip, limit)
    return ListVacancyResponse(
        Vacancies=[VacancyResponse.from_orm(v) for v in vacancies],
    )


@vacancy_router.get("/search", status_code=200)
async def search_vacancies(
    query: str,
    skip: int = 0,
    limit: int = 10,
    vacancy_controller: VacancyController = Depends(Factory().get_vacancy_controller),
) -> ListVacancyResponse:
    vacancies = await vacancy_controller.search_vacancies(query=query, skip=skip, limit=limit)
    return ListVacancyResponse(
        Vacancies=[VacancyResponse.from_orm(v) for v in vacancies],
    )


@vacancy_router.get(
    "/get_my",
    dependencies=[Depends(AuthenticationRequired)],
    status_code=200,
)
@Cache.cached(prefix="vacancy:me", ttl=60)
async def get_my_vacancies(
    user: User = Depends(get_current_user),
    vacancy_controller: VacancyController = Depends(Factory().get_vacancy_controller),
) -> ListVacancyResponse:
    vacancies = await vacancy_controller.get_by_user(user)
    return ListVacancyResponse(
        Vacancies=[VacancyResponse.from_orm(v) for v in vacancies],
    )


@vacancy_router.get(
    "/{vacancy_uuid}",
    status_code=200,
)
@Cache.cached(prefix="vacancy:uuid", ttl=60)
async def get_vacancy(
    vacancy_uuid: UUID,
    vacancy_controller: VacancyController = Depends(Factory().get_vacancy_controller),
) -> VacancyResponse:
    vacancy = await vacancy_controller.get_by_uuid(uuid=vacancy_uuid, join_={"employment_types"})
    return VacancyResponse.from_orm(vacancy[0])


@vacancy_router.patch(
    "/edit/{vacancy_uuid}",
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
    vacancy: Vacancy = await vacancy_controller.update_by_uuid(
        user=user,
        uuid=vacancy_uuid,
        attrs=edit_vacancy_request.model_dump(exclude_unset=True),
    )
    await Cache.remove_by_prefix("vacancy:all")
    await Cache.remove_by_prefix(f"vacancy:me:{user.o_id}")
    await Cache.remove_by_prefix(f"vacancy:uuid:{vacancy_uuid}")
    return VacancyResponse.from_orm(vacancy)


@vacancy_router.delete(
    "/{vacancy_uuid}",
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
    await vacancy_controller.delete_by_uuid(user, vacancy_uuid)
    await Cache.remove_by_prefix("vacancy:all")
    await Cache.remove_by_prefix(f"vacancy:me:{user.o_id}")
    await Cache.remove_by_prefix("vacancy:uuid")
