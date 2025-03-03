from sqlalchemy import select

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
