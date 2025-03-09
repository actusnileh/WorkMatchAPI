from sqlalchemy import select
from sqlalchemy.orm import joinedload

from app.models import (
    EmploymentType,
    Specialist,
)
from core.repository import BaseRepository


class SpecialistRepository(BaseRepository[Specialist]):
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

    async def get_by_uuid(self, uuid) -> Specialist:
        query = (
            select(Specialist)
            .options(joinedload(Specialist.employment_type))
            .filter(Specialist.uuid == uuid)
        )
        result = await self.session.execute(query)
        return result.scalars().one_or_none()
