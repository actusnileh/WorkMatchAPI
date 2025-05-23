from uuid import UUID

from fastapi import (
    APIRouter,
    Depends,
)

from app.controllers import SpecialistController
from app.models import (
    Specialist,
    User,
)
from app.schemas.requests.specialist import (
    AddExperienceSpecialistRequest,
    AddSkillSpecialistRequest,
    EditSpecialistRequest,
    SpecialistRequest,
)
from app.schemas.responses.specialist import (
    ListSpecialistResponseWithAdditional,
    SpecialistResponse,
    SpecialistResponseWithAdditional,
)
from core.factory.factory import Factory
from core.fastapi.dependencies.authentication import AuthenticationRequired
from core.fastapi.dependencies.current_user import get_current_user
from core.fastapi.dependencies.role_required import RoleRequired


specialist_router = APIRouter()


@specialist_router.get(
    "/{specialist_uuid}",
    dependencies=[Depends(AuthenticationRequired)],
    summary="Получить информацию о специалисте",
    status_code=200,
)
async def get_specialist_by_uuid(
    specialist_uuid: UUID,
    specialist_controller: SpecialistController = Depends(Factory().get_specialist_controller),
) -> SpecialistResponseWithAdditional:
    """
    Возвращает информацию о специалисте по его UUID.
    """
    specialist: Specialist = await specialist_controller.get_by_uuid(specialist_uuid)
    return SpecialistResponseWithAdditional.from_orm(specialist)


@specialist_router.get(
    "/",
    dependencies=[Depends(AuthenticationRequired)],
    summary="Получить специалистов текущего пользователя",
    status_code=200,
)
async def get_my_specialists(
    user: User = Depends(get_current_user),
    specialist_controller: SpecialistController = Depends(Factory().get_specialist_controller),
) -> ListSpecialistResponseWithAdditional:
    """
    Возвращает список специалистов, связанных с текущим пользователем.
    """
    specialists = await specialist_controller.get_by_user(user)
    return ListSpecialistResponseWithAdditional(
        Specialists=[SpecialistResponseWithAdditional.from_orm(s) for s in specialists],
    )


@specialist_router.post(
    "/",
    dependencies=[
        Depends(AuthenticationRequired),
        Depends(RoleRequired(["user", "admin"])),
    ],
    summary="Создать нового специалиста",
    status_code=201,
)
async def create_specialist(
    create_specialist_request: SpecialistRequest,
    user: User = Depends(get_current_user),
    specialist_controller: SpecialistController = Depends(Factory().get_specialist_controller),
) -> SpecialistResponse:
    """
    Создает нового специалиста, связанного с текущим пользователем.
    """
    specialist, employment_type = await specialist_controller.create_specialist(
        created_by=user,
        position=create_specialist_request.position,
        about_me=create_specialist_request.about_me,
        employment_type_str=create_specialist_request.employment_type_str,
    )
    return SpecialistResponse.from_orm(specialist, employment_type)


@specialist_router.patch(
    "/edit/{specialist_uuid}",
    dependencies=[
        Depends(AuthenticationRequired),
        Depends(RoleRequired(["user", "admin"])),
    ],
    summary="Редактировать информацию о специалисте",
    status_code=200,
)
async def edit_specialist(
    specialist_uuid: UUID,
    edit_specialist_request: EditSpecialistRequest,
    user: User = Depends(get_current_user),
    specialist_controller: SpecialistController = Depends(Factory().get_specialist_controller),
) -> SpecialistResponse:
    """
    Редактирует информацию о специалисте по его UUID.
    """
    specialist: Specialist = await specialist_controller.update_by_uuid(
        user=user,
        uuid=specialist_uuid,
        attrs=edit_specialist_request.model_dump(exclude_unset=True),
    )
    return SpecialistResponse.from_orm(specialist)


@specialist_router.post(
    "/{specialist_uuid}/skill",
    dependencies=[
        Depends(AuthenticationRequired),
        Depends(RoleRequired(["user", "admin"])),
    ],
    summary="Добавить навык специалисту",
    status_code=200,
)
async def add_skill(
    specialist_uuid: UUID,
    add_skill_specialist_request: AddSkillSpecialistRequest,
    user: User = Depends(get_current_user),
    specialist_controller: SpecialistController = Depends(Factory().get_specialist_controller),
) -> SpecialistResponseWithAdditional:
    """
    Добавляет новый навык специалисту.
    """
    response = await specialist_controller.add_skill(
        user,
        specialist_uuid,
        add_skill_specialist_request.skill,
    )
    return SpecialistResponseWithAdditional.from_orm(response)


@specialist_router.delete(
    "/{specialist_uuid}/skill/{skill}",
    dependencies=[
        Depends(AuthenticationRequired),
        Depends(RoleRequired(["user", "admin"])),
    ],
    summary="Удалить навык специалиста",
    status_code=200,
)
async def remove_skill(
    specialist_uuid: UUID,
    skill: str,
    user: User = Depends(get_current_user),
    specialist_controller: SpecialistController = Depends(Factory().get_specialist_controller),
) -> SpecialistResponseWithAdditional:
    """
    Удаляет навык у специалиста.
    """
    response = await specialist_controller.remove_skill(
        user,
        specialist_uuid,
        skill,
    )
    return SpecialistResponseWithAdditional.from_orm(response)


@specialist_router.post(
    "/{specialist_uuid}/experience",
    dependencies=[
        Depends(AuthenticationRequired),
        Depends(RoleRequired(["user", "admin"])),
    ],
    summary="Добавить опыт работы специалисту",
    status_code=200,
)
async def add_experience(
    specialist_uuid: UUID,
    add_experience_specialist_request: AddExperienceSpecialistRequest,
    user: User = Depends(get_current_user),
    specialist_controller: SpecialistController = Depends(Factory().get_specialist_controller),
) -> SpecialistResponseWithAdditional:
    """
    Добавляет новый опыт работы специалисту.
    """
    response = await specialist_controller.add_experience(
        user,
        specialist_uuid,
        add_experience_specialist_request.company_name,
        add_experience_specialist_request.position,
        add_experience_specialist_request.start_date,
        add_experience_specialist_request.end_date,
    )
    return SpecialistResponseWithAdditional.from_orm(response)


@specialist_router.delete(
    "/{specialist_uuid}/experience/{experience_uuid}",
    dependencies=[
        Depends(AuthenticationRequired),
        Depends(RoleRequired(["user", "admin"])),
    ],
    summary="Удалить опыт работы специалиста",
    status_code=200,
)
async def remove_experience(
    specialist_uuid: UUID,
    experience_uuid: UUID,
    user: User = Depends(get_current_user),
    specialist_controller: SpecialistController = Depends(Factory().get_specialist_controller),
) -> SpecialistResponseWithAdditional:
    """
    Удаляет указанный опыт работы у специалиста.
    """
    response = await specialist_controller.remove_experience(
        user,
        specialist_uuid,
        experience_uuid,
    )
    return SpecialistResponseWithAdditional.from_orm(response)


@specialist_router.delete(
    "/{specialist_uuid}",
    dependencies=[
        Depends(AuthenticationRequired),
        Depends(RoleRequired(["user", "admin"])),
    ],
    summary="Удалить специалиста",
    status_code=204,
)
async def delete_specialist(
    specialist_uuid: UUID,
    user: User = Depends(get_current_user),
    specialist_controller: SpecialistController = Depends(Factory().get_specialist_controller),
) -> None:
    """
    Удаляет специалиста по его UUID.
    """
    await specialist_controller.delete_by_uuid(user, specialist_uuid)
