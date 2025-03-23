from fastapi import (
    HTTPException,
    status,
)

from pydantic import UUID4

from app.models import (
    User,
    Vacancy,
)
from app.repositories import VacancyRepository
from core.controller import BaseController
from core.database import Transactional
from core.exceptions import BadRequestException
from core.utils.datetime_util import utcnow


class VacancyController(BaseController[Vacancy]):
    def __init__(self, vacancy_repository: VacancyRepository):
        super().__init__(model=Vacancy, repository=vacancy_repository)
        self.vacancy_repository = vacancy_repository

    @Transactional()
    async def create_vacancy(
        self,
        title: str,
        description: str,
        requirements: str,
        conditions: str,
        salary: float,
        created_by: User,
        employment_type_str: str,
    ) -> Vacancy:
        employment_type = await self.vacancy_repository.get_employment_type_by_name(
            employment_type_str,
        )
        if not employment_type:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Указанный тип занятости не найден. Возможные значения: full-time, part-time.",
            )
        vacancy: Vacancy = await self.vacancy_repository.get_by_filters(
            title=title,
            description=description,
        )

        if vacancy:
            raise BadRequestException("Такая вакансия уже существует")

        return await self.vacancy_repository.create(
            {
                "title": title,
                "description": description,
                "requirements": requirements,
                "conditions": conditions,
                "salary": salary,
                "created_by": created_by.o_id,
                "employment_type": employment_type,
            },
        )

    async def get_all(self, skip: int = 0, limit: int = 100) -> list[Vacancy]:
        return await self.vacancy_repository.get_all(skip=skip, limit=limit, join_={"employment_types"})

    @Transactional()
    async def update_by_uuid(self, user: User, uuid: UUID4, attrs: dict) -> User:
        attrs["updated_at"] = utcnow()
        vacancy: Vacancy = await self.vacancy_repository.get_by_uuid(uuid=uuid)
        if not vacancy:
            raise BadRequestException("По указанному UUID не найдена вакансия")
        if user.o_id != vacancy.created_by:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Недостаточно прав для редактирования вакансии '{vacancy.title}'.",
            )

        return await self.vacancy_repository._update(vacancy, attrs)

    async def get_by_user(self, user: User):
        vacancies = await self.vacancy_repository.get_by(
            field="created_by",
            value=user.o_id,
            join_={"employment_types"},
            unique=False,
        )
        if len(vacancies) == 0:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="У вас нет вакансий.",
            )
        return vacancies
