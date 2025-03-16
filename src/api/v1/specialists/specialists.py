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
    SpecialistResponse,
    SpecialistResponseWithAdditional,
)
from core.factory.factory import Factory
from core.fastapi.dependencies.authentication import AuthenticationRequired
from core.fastapi.dependencies.current_user import get_current_user
from core.fastapi.dependencies.role_required import RoleRequired


specialist_router = APIRouter()


@specialist_router.post(
    "/",
    dependencies=[
        Depends(AuthenticationRequired),
        Depends(RoleRequired(["user", "admin"])),
    ],
    status_code=201,
)
async def create_specialist(
    create_specialist_request: SpecialistRequest,
    user: User = Depends(get_current_user),
    specialist_controller: SpecialistController = Depends(
        Factory().get_specialist_controller,
    ),
) -> SpecialistResponse:
    specialist: Specialist = await specialist_controller.create_specialist(
        created_by=user,
        position=create_specialist_request.position,
        about_me=create_specialist_request.about_me,
        employment_type_str=create_specialist_request.employment_type_str,
    )

    return SpecialistResponse.from_orm(specialist)


@specialist_router.patch(
    "/edit/{specialist_uuid}",
    dependencies=[
        Depends(AuthenticationRequired),
        Depends(RoleRequired(["user", "admin"])),
    ],
    status_code=200,
)
async def edit_specialist(
    specialist_uuid: str,
    edit_specialist_request: EditSpecialistRequest,
    user: User = Depends(get_current_user),
    specialist_controller: SpecialistController = Depends(
        Factory().get_specialist_controller,
    ),
) -> SpecialistResponse:
    specialsit: Specialist = await specialist_controller.update_by_uuid(
        user=user,
        uuid=specialist_uuid,
        attrs=edit_specialist_request.model_dump(exclude_unset=True),
    )

    return SpecialistResponse.from_orm(specialsit)


@specialist_router.post(
    "/{specialist_uuid}/skill",
    dependencies=[
        Depends(AuthenticationRequired),
        Depends(RoleRequired(["user", "admin"])),
    ],
    status_code=200,
)
async def add_skill(
    specialist_uuid: str,
    add_skill_specialist_request: AddSkillSpecialistRequest,
    user: User = Depends(get_current_user),
    specialist_controller: SpecialistController = Depends(
        Factory().get_specialist_controller,
    ),
) -> SpecialistResponseWithAdditional:
    return SpecialistResponseWithAdditional.from_orm(
        await specialist_controller.add_skill(
            user,
            specialist_uuid,
            add_skill_specialist_request.skill,
        ),
    )


@specialist_router.delete(
    "/{specialist_uuid}/skill/{skill}",
    dependencies=[
        Depends(AuthenticationRequired),
        Depends(RoleRequired(["user", "admin"])),
    ],
    status_code=200,
)
async def remove_skill(
    specialist_uuid: str,
    skill: str,
    user: User = Depends(get_current_user),
    specialist_controller: SpecialistController = Depends(
        Factory().get_specialist_controller,
    ),
) -> SpecialistResponseWithAdditional:
    return SpecialistResponseWithAdditional.from_orm(
        await specialist_controller.remove_skill(
            user,
            specialist_uuid,
            skill,
        ),
    )


@specialist_router.post(
    "/{specialist_uuid}/experience",
    dependencies=[
        Depends(AuthenticationRequired),
        Depends(RoleRequired(["user", "admin"])),
    ],
    status_code=200,
)
async def add_experience(
    specialist_uuid: str,
    add_experience_specialist_request: AddExperienceSpecialistRequest,
    user: User = Depends(get_current_user),
    specialist_controller: SpecialistController = Depends(
        Factory().get_specialist_controller,
    ),
) -> SpecialistResponseWithAdditional:
    return SpecialistResponseWithAdditional.from_orm(
        await specialist_controller.add_experience(
            user,
            specialist_uuid,
            add_experience_specialist_request.company_name,
            add_experience_specialist_request.position,
            add_experience_specialist_request.start_date,
            add_experience_specialist_request.end_date,
        ),
    )


@specialist_router.delete(
    "/{specialist_uuid}/experience/{experience_uuid}",
    dependencies=[
        Depends(AuthenticationRequired),
        Depends(RoleRequired(["user", "admin"])),
    ],
    status_code=200,
)
async def remove_experience(
    specialist_uuid: str,
    experience_uuid: str,
    user: User = Depends(get_current_user),
    specialist_controller: SpecialistController = Depends(
        Factory().get_specialist_controller,
    ),
) -> SpecialistResponseWithAdditional:
    return SpecialistResponseWithAdditional.from_orm(
        await specialist_controller.remove_experience(
            user,
            specialist_uuid,
            experience_uuid,
        ),
    )
