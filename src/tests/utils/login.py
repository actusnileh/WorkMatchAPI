from typing import Any

from httpx import AsyncClient

from tests.factory.users import (
    create_fake_hr,
    create_fake_user,
)


async def _create_user_and_login(
    client: AsyncClient,
    fake_user=create_fake_user(),
) -> dict[str, Any]:
    await client.post("/v1/users/", json=fake_user)

    response = await client.post("/v1/users/login", json=fake_user)
    access_token = response.json()["access_token"]

    client.headers.update({"Authorization": f"Bearer {access_token}"})

    return fake_user


async def _create_hr_and_login(
    client: AsyncClient,
    fake_user=create_fake_hr(),
) -> dict[str, Any]:
    await client.post("/v1/users/", json=fake_user)

    response = await client.post("/v1/users/login", json=fake_user)
    access_token = response.json()["access_token"]

    client.headers.update({"Authorization": f"Bearer {access_token}"})

    return fake_user


__all__ = ["_create_user_and_login", "_create_hr_and_login"]
