import pytest
import pytest_asyncio
from faker import Faker

from app.models import User
from app.models.role import Role
from core.repository import BaseRepository


fake = Faker()


class TestBaseRepository:
    @pytest_asyncio.fixture
    async def repository(self, db_session):
        return BaseRepository(model=User, db_session=db_session)

    @pytest_asyncio.fixture
    async def role(self, db_session):
        role = await db_session.execute(Role.__table__.select().where(Role.name == "user"))
        role = role.scalar()
        return role

    @pytest.mark.asyncio
    async def test_create(self, repository, role):
        user_data = self._user_data_generator(role)
        user = await repository.create(user_data)
        assert user.username is not None

    @pytest.mark.asyncio
    async def test_get_all(self, repository, role):
        await repository.create(self._user_data_generator(role))
        await repository.create(self._user_data_generator(role))
        users = await repository.get_all()
        assert len(users) == 2

    def _user_data_generator(self, role):
        return {
            "email": fake.email(),
            "username": fake.user_name(),
            "password": fake.password(),
            "full_name": fake.name(),
            "role_id": role,
        }
