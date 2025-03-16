from sqlalchemy import select
from sqlalchemy.orm import joinedload

from app.models import (
    EmploymentType,
    Vacancy,
)
from core.repository import BaseRepository


class VacancyRepository(BaseRepository[Vacancy]):

    async def get_employment_type_by_name(
        self,
        name: str,
        join_: set[str] | None = None,
    ) -> EmploymentType | None:
        query = select(EmploymentType)
        query = self._maybe_join(query, join_)
        query = query.filter(EmploymentType.name == name)

        if join_ is not None:
            return await self._all_unique(query)

        return await self._one_or_none(query)

    async def get_by_uuid(self, uuid) -> Vacancy:
        query = select(Vacancy).options(joinedload(Vacancy.employment_type)).filter(Vacancy.uuid == uuid)
        result = await self.session.execute(query)
        return result.scalars().one_or_none()
