from fastapi import (
    HTTPException,
    status,
)

from sqlalchemy.exc import IntegrityError

from app.models import (
    Application,
    User,
)
from app.repositories import ApplicationRepository
from app.repositories.specialist import SpecialistRepository
from app.repositories.vacancy import VacancyRepository
from app.schemas.responses.specialist import SpecialistResponseWithAdditional
from app.schemas.responses.vacancy import VacancyResponse
from core.controller import BaseController
from worker.worker import apply_neural_network


class ApplicationController(BaseController[Application]):
    def __init__(
        self,
        application_repository: ApplicationRepository,
        specialist_repository: SpecialistRepository,
        vacancy_repository: VacancyRepository,
    ):
        super().__init__(model=Application, repository=application_repository)
        self.application_repository = application_repository
        self.specialist_repository = specialist_repository
        self.vacancy_repository = vacancy_repository

    async def create(self, user: User, specialist_uuid: str, vacancy_uuid: str) -> Application:
        specialist = await self.specialist_repository.get_by_uuid(specialist_uuid)
        if not specialist:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="По указанному UUID не найдено резюме.",
            )

        if specialist.created_by != user.o_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Недостаточно прав для создания заявки на вакансию.",
            )

        vacancy = await self.vacancy_repository.get_by_uuid(vacancy_uuid)
        if not vacancy:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="По указанному UUID не найдена вакансия.",
            )

        try:
            application = await self.application_repository.create(
                {
                    "specialist_uuid": specialist.uuid,
                    "vacancy_uuid": vacancy.uuid,
                },
            )
        except IntegrityError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Заявка на данную вакансию уже существует.",
            )
        else:
            vacancy_schema = VacancyResponse.from_orm(vacancy)
            specialist_schema = SpecialistResponseWithAdditional.from_orm(specialist)
            vacancy_json = vacancy_schema.model_dump(mode="json", exclude_none=True, exclude_unset=True)
            specialst_json = specialist_schema.model_dump(mode="json", exclude_none=True, exclude_unset=True)
            apply_neural_network.apply_async((vacancy_json, specialst_json))

        return application

    async def delete_by_specialist(self, user: User, specialist_uuid: str, vacancy_uuid: str):
        application = await self.application_repository.get_by_specialist_vacancy(
            specialist_uuid,
            vacancy_uuid,
        )
        if not application:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Заявка на данную вакансию не найдена.",
            )

        if application.specialist.created_by != user.o_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Недостаточно прав для удаления заявки на вакансию.",
            )

        await self.application_repository.delete(application)

    async def get_by_specialist(self, specialist_uuid: str, vacancy_uuid: str) -> Application:
        application = await self.application_repository.get_by_specialist_vacancy(
            specialist_uuid,
            vacancy_uuid,
        )
        if not application:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Заявка на данную вакансию не найдена.",
            )

        return application

    async def get_all_by_specialist(self, specialist_uuid: str) -> list[Application]:
        applications = await self.application_repository.get_by(
            field="specialist_uuid",
            value=specialist_uuid,
        )
        return applications

    async def get_all_by_vacancy(self, vacancy_uuid: str) -> list[Application]:
        applications = await self.application_repository.get_by(
            field="vacancy_uuid",
            value=vacancy_uuid,
        )
        return applications
