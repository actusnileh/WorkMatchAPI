import os

import pytest_asyncio
from sqlalchemy import insert
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    create_async_engine,
)
from sqlalchemy.orm import sessionmaker

import core.database.transactional as transactional
from app.models import Base
from app.models.employment_type import EmploymentType
from app.models.role import Role
from core.config import config


TEST_DATABASE_URL = os.getenv("TEST_POSTGRES_URL")

config.POSTGRES_URL = TEST_DATABASE_URL


@pytest_asyncio.fixture(scope="function")
async def db_session() -> AsyncSession:
    async_engine = create_async_engine(config.POSTGRES_URL)
    session = sessionmaker(async_engine, class_=AsyncSession, expire_on_commit=False)

    async with session() as s:
        async with async_engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

        await s.execute(
            insert(Role).values(
                [
                    {"name": "hr"},
                    {"name": "admin"},
                    {"name": "user"},
                ],
            ),
        )
        await s.execute(
            insert(EmploymentType).values(
                [
                    {"name": "full-time"},
                    {"name": "part-time"},
                ],
            ),
        )
        await s.commit()

        transactional.session = s
        yield s

    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

    await async_engine.dispose()
