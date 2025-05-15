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
from core.elasticsearch import es_client
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
            join_={"employment_types"},
        )

        if vacancy:
            raise BadRequestException("Такая вакансия уже существует")

        created_vacancy = await self.vacancy_repository.create(
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

        created_vacancy = await self.vacancy_repository.get_by(
            field="uuid",
            value=created_vacancy.uuid,
            join_={"employment_types"},
            unique=True,
        )

        await self.index_vacancy(created_vacancy)

        return created_vacancy

    async def get_all(self, skip: int = 0, limit: int = 100) -> tuple[list[Vacancy], int]:
        return await self.vacancy_repository.get_all(skip=skip, limit=limit, join_={"employment_types"})

    @Transactional()
    async def update_by_uuid(self, user: User, uuid: UUID4, attrs: dict) -> Vacancy:
        attrs["updated_at"] = utcnow()

        vacancy: Vacancy = await self.vacancy_repository.get_by_uuid(uuid=uuid)
        if not vacancy:
            raise BadRequestException("По указанному UUID не найдена вакансия")
        if user.o_id != vacancy.created_by:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Недостаточно прав для редактирования вакансии '{vacancy.title}'.",
            )

        if "employment_type_str" in attrs:
            employment_type = await self.vacancy_repository.get_employment_type_by_name(
                attrs.pop("employment_type_str")
            )
            if not employment_type:
                raise BadRequestException("Указанный тип занятости не найден.")
            attrs["employment_type"] = employment_type

        updated_vacancy = await self.vacancy_repository._update(vacancy, attrs)

        await self.index_vacancy(updated_vacancy)

        return updated_vacancy

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

    async def delete_by_uuid(self, user, uuid: str):
        vacancy: Vacancy = await self.vacancy_repository.get_by_uuid(uuid=uuid)
        if not vacancy:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="По указанному UUID не найдена вакансия.",
            )
        if user.o_id != vacancy.created_by:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Недостаточно прав для удаления данной вакансии.",
            )
        await self.vacancy_repository.delete(vacancy)

        await self.delete_vacancy_from_index(vacancy.id)

    async def search_vacancies(self, query: str, skip: int = 0, limit: int = 10) -> list[Vacancy]:
        body = {
            "query": {
                "multi_match": {"query": query, "fields": ["title", "description", "requirements", "conditions"]},
            },
            "from": skip,
            "size": limit,
        }
        response = await es_client.search(index="vacancies", body=body)
        hits = response["hits"]["hits"]

        vacancies = [Vacancy(**hit["_source"]) for hit in hits]

        for vacancy in vacancies:
            if vacancy.employment_type_id:
                vacancy.employment_type = await self.vacancy_repository.get_employment_type_by_id(
                    vacancy.employment_type_id,
                )

        return vacancies

    async def index_vacancy(self, vacancy: Vacancy) -> None:
        """
        Индексация вакансии в Elasticsearch.
        """
        vacancy = vacancy[0] if isinstance(vacancy, list) else vacancy
        document = {
            "o_id": vacancy.o_id,
            "uuid": str(vacancy.uuid),
            "title": vacancy.title,
            "description": vacancy.description,
            "requirements": vacancy.requirements,
            "conditions": vacancy.conditions,
            "salary": vacancy.salary,
            "employment_type_id": vacancy.employment_type_id,
        }
        await es_client.index(index="vacancies", id=vacancy.o_id, document=document)

    async def delete_vacancy_from_index(self, vacancy_id: int) -> None:
        """
        Удаление вакансии из индекса Elasticsearch.
        """
        await es_client.delete(index="vacancies", id=vacancy_id)
