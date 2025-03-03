from app.models import (
    User,
    Vacancy,
)
from app.repositories import VacancyRepository
from core.controller import BaseController
from core.database import Transactional
from core.exceptions import BadRequestException


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
            raise BadRequestException(
                "Указанный тип занятости не найден. Возможные значения: full-time, part-time",
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
