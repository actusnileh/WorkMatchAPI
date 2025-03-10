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
    EditSpecialistRequest,
    SpecialistRequest,
)
from app.schemas.responses.specialist import SpecialistResponse
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
