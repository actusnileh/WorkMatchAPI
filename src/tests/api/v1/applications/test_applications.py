import pytest
import pytest_asyncio
from faker import Faker
from httpx import AsyncClient

from tests.utils.login import (
    _create_hr_and_login,
    _create_user_and_login,
)


@pytest_asyncio.fixture
async def create_vacancy(client: AsyncClient, faker: Faker) -> None:
    await _create_hr_and_login(client)
    vacancy_json = {
        "title": faker.job(),
        "description": faker.text(max_nb_chars=200),
        "requirements": faker.paragraph(nb_sentences=3),
        "conditions": "free jobs",
        "salary": faker.random_int(min=30000, max=100000),
        "employment_type_str": faker.random_element(["full-time", "part-time"]),
    }
    response = await client.post(
        "/v1/vacancies/",
        json=vacancy_json,
    )
    assert response.status_code == 201
    assert response.json()["title"] == vacancy_json["title"]
    assert response.json()["description"] == vacancy_json["description"]
    assert response.json()["requirements"] == vacancy_json["requirements"]

    return response.json()


@pytest_asyncio.fixture
async def create_specialist(client: AsyncClient, faker: Faker) -> None:
    await _create_user_and_login(client)
    specialist_json = {
        "position": "junior",
        "about_me": faker.text(max_nb_chars=160),
        "employment_type_str": "full-time",
    }

    response = await client.post(
        "/v1/specialist/",
        json=specialist_json,
    )

    assert response.status_code == 201
    assert response.json()["position"] == specialist_json["position"]
    assert response.json()["about_me"] == specialist_json["about_me"]

    return response.json()


@pytest.mark.asyncio
async def test_create_application(client: AsyncClient, create_vacancy, create_specialist) -> None:
    vacancy = create_vacancy
    specialist = create_specialist
    response = await client.post(
        f"/v1/applications/{specialist['uuid']}/{vacancy['uuid']}",
    )
    assert response.status_code == 201
    assert response.json()["vacancy_uuid"] == vacancy["uuid"]
    assert response.json()["specialist_uuid"] == specialist["uuid"]


@pytest.mark.asyncio
async def test_get_applications(client: AsyncClient, create_vacancy, create_specialist) -> None:
    vacancy = create_vacancy
    specialist = create_specialist
    await client.post(
        f"/v1/applications/{specialist['uuid']}/{vacancy['uuid']}",
    )

    response = await client.get(
        f"/v1/applications/{specialist['uuid']}/{vacancy['uuid']}",
    )

    assert response.status_code == 200
    assert response.json()["vacancy_uuid"] == vacancy["uuid"]
    assert response.json()["specialist_uuid"] == specialist["uuid"]


@pytest.mark.asyncio
async def test_delete_application(client: AsyncClient, create_vacancy, create_specialist) -> None:
    vacancy = create_vacancy
    specialist = create_specialist
    await client.post(
        f"/v1/applications/{specialist['uuid']}/{vacancy['uuid']}",
    )

    response = await client.delete(
        f"/v1/applications/{specialist['uuid']}/{vacancy['uuid']}",
    )

    assert response.status_code == 204

    response = await client.get(
        f"/v1/applications/{specialist['uuid']}/{vacancy['uuid']}",
    )

    assert response.status_code == 404


@pytest.mark.asyncio
async def test_get_applications_failed_with_invalid_uuid_or_auth(
    client: AsyncClient,
) -> None:
    response = await client.get(
        "/v1/applications/invalid_uuid/invalid_uuid",
    )

    assert response.status_code == 401


@pytest.mark.asyncio
async def test_delete_application_failed_with_invalid_uuid_or_auth(
    client: AsyncClient,
) -> None:
    response = await client.delete(
        "/v1/applications/invalid_uuid/invalid_uuid",
    )

    assert response.status_code == 401


@pytest.mark.asyncio
async def test_create_application_failed_with_invalid_uuid_or_auth(
    client: AsyncClient,
) -> None:
    response = await client.post(
        "/v1/applications/invalid_uuid/invalid_uuid",
    )

    assert response.status_code == 401
