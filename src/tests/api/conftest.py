from typing import (
    Any,
    Generator,
)

from fastapi import FastAPI

import pytest
import pytest_asyncio
from httpx import (
    ASGITransport,
    AsyncClient,
)

from core.factory.factory import get_session
from core.server import create_app


@pytest.fixture(scope="session")
def app() -> Generator[FastAPI, Any, None]:
    """
    Create a new FastAPI app
    """
    app = create_app()

    yield app


@pytest_asyncio.fixture(scope="function")
async def client(app: FastAPI, db_session) -> AsyncClient:
    """
    Create a new FastAPI AsyncClient
    """

    async def _get_session():
        return db_session

    app.dependency_overrides[get_session] = _get_session

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        yield client
