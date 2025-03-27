from uuid import UUID

from fastapi import (
    APIRouter,
    Depends,
)

from app.controllers import ApplicationController
from app.models.user import User
from app.schemas.responses.application import (
    ApplicationResponse,
    ListApplicationResponse,
)
from core.factory import Factory
from core.fastapi.dependencies.authentication import AuthenticationRequired
from core.fastapi.dependencies.current_user import get_current_user
from core.fastapi.dependencies.role_required import RoleRequired


application_router = APIRouter()


@application_router.get("/specialist/{specialist_uuid}")
async def get_all_applications_by_specialist(
    specialist_uuid: UUID,
    application_controller: ApplicationController = Depends(Factory().get_application_controller),
) -> ListApplicationResponse:
    applications = await application_controller.get_all_by_specialist(specialist_uuid)
    return ListApplicationResponse(applications=[ApplicationResponse.from_orm(a) for a in applications])


@application_router.get("/vacancy/{vacancy_uuid}")
async def get_all_applications_by_vacancy(
    vacancy_uuid: UUID,
    application_controller: ApplicationController = Depends(Factory().get_application_controller),
) -> ListApplicationResponse:
    applications = await application_controller.get_all_by_vacancy(vacancy_uuid)
    return ListApplicationResponse(applications=[ApplicationResponse.from_orm(a) for a in applications])


@application_router.post(
    "/{specialist_uuid}/{vacancy_uuid}",
    status_code=201,
    dependencies=[
        Depends(AuthenticationRequired),
        Depends(RoleRequired(["user", "admin"])),
    ],
)
async def application(
    specialist_uuid: UUID,
    vacancy_uuid: UUID,
    user: User = Depends(get_current_user),
    application_controller: ApplicationController = Depends(Factory().get_application_controller),
) -> ApplicationResponse:
    application = await application_controller.create(user, specialist_uuid, vacancy_uuid)
    return ApplicationResponse.from_orm(application)


@application_router.get(
    "/{specialist_uuid}/{vacancy_uuid}",
    dependencies=[
        Depends(AuthenticationRequired),
    ],
)
async def get_application(
    specialist_uuid: UUID,
    vacancy_uuid: UUID,
    application_controller: ApplicationController = Depends(Factory().get_application_controller),
) -> ApplicationResponse:
    application = await application_controller.get_by_specialist(specialist_uuid, vacancy_uuid)
    return ApplicationResponse.from_orm(application)


@application_router.delete(
    "/{specialist_uuid}/{vacancy_uuid}",
    dependencies=[
        Depends(AuthenticationRequired),
    ],
    status_code=204,
)
async def delete_application(
    specialist_uuid: UUID,
    vacancy_uuid: UUID,
    user: User = Depends(get_current_user),
    application_controller: ApplicationController = Depends(Factory().get_application_controller),
) -> None:
    await application_controller.delete_by_specialist(user, specialist_uuid, vacancy_uuid)
