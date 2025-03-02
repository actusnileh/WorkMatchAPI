from sqlalchemy import select
from sqlalchemy.orm import selectinload

from app.models import (
    EmploymentType,
    Role,
    User,
)
from core.repository import BaseRepository


class UserRepository(BaseRepository[User]):
    async def get_by_username(
        self,
        username: str,
        join_: set[str] | None = None,
    ) -> User | None:
        query = self._query(join_)
        query = query.filter(User.username == username)

        if join_ is not None:
            return await self.all_unique(query)

        return await self._one_or_none(query)

    async def get_by_email(
        self,
        email: str,
        join_: set[str] | None = None,
    ) -> User | None:
        query = self._query(join_)
        query = query.filter(User.email == email)

        if join_ is not None:
            return await self.all_unique(query)

        return await self._one_or_none(query)

    async def get_role_by_name(
        self,
        name: str,
        join_: set[str] | None = None,
    ) -> Role | None:
        query = select(Role)
        query = self._maybe_join(query, join_)
        query = query.filter(Role.name == name)

        if join_ is not None:
            return await self._all_unique(query)

        return await self._one_or_none(query)

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

    def _join_role(self, query):
        return query.join(User.role).options(selectinload(User.role))
