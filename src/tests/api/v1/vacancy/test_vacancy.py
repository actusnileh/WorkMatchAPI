import pytest
from faker import Faker
from httpx import AsyncClient

from tests.utils.login import _create_hr_and_login


@pytest.mark.asyncio
async def test_create_vacancy(client: AsyncClient) -> None:
    fake = Faker()
    await _create_hr_and_login(client)
    vacancy_json = {
        "title": fake.job(),
        "description": fake.text(max_nb_chars=200),
        "requirements": fake.paragraph(nb_sentences=3),
        "conditions": "free jobs",
        "salary": fake.random_int(min=30000, max=100000),
        "employment_type_str": fake.random_element(["full-time", "part-time"]),
    }
    response = await client.post(
        "/v1/vacancies/",
        json=vacancy_json,
    )
    assert response.status_code == 201
    assert response.json()["title"] == vacancy_json["title"]
    assert response.json()["description"] == vacancy_json["description"]
    assert response.json()["requirements"] == vacancy_json["requirements"]


@pytest.mark.asyncio
async def test_create_vacancy_with_invalid_employment_type(client: AsyncClient) -> None:
    fake = Faker()
    await _create_hr_and_login(client)
    vacancy_json = {
        "title": fake.job(),
        "description": fake.text(max_nb_chars=200),
        "requirements": fake.paragraph(nb_sentences=3),
        "conditions": "free jobs",
        "salary": fake.random_int(min=30000, max=100000),
        "employment_type_str": fake.random_element(["asd", "das"]),
    }
    response = await client.post(
        "/v1/vacancies/",
        json=vacancy_json,
    )
    assert response.status_code == 400


@pytest.mark.asyncio
async def test_get_vacancies(client: AsyncClient) -> None:
    fake = Faker()
    await _create_hr_and_login(client)
    vacancy_json = {
        "title": fake.job(),
        "description": fake.text(max_nb_chars=200),
        "requirements": fake.paragraph(nb_sentences=3),
        "conditions": "free jobs",
        "salary": fake.random_int(min=30000, max=100000),
        "employment_type_str": fake.random_element(["full-time", "part-time"]),
    }
    await client.post(
        "/v1/vacancies/",
        json=vacancy_json,
    )

    response = await client.get("/v1/vacancies/")
    assert response.status_code == 200
    assert len(response.json()["Vacancies"]) > 0


@pytest.mark.asyncio
async def test_get_my_vacancies(client: AsyncClient) -> None:
    fake = Faker()
    await _create_hr_and_login(client)
    vacancy_json = {
        "title": fake.job(),
        "description": fake.text(max_nb_chars=200),
        "requirements": fake.paragraph(nb_sentences=3),
        "conditions": "free jobs",
        "salary": fake.random_int(min=30000, max=100000),
        "employment_type_str": fake.random_element(["full-time", "part-time"]),
    }
    response = await client.post(
        "/v1/vacancies/",
        json=vacancy_json,
    )
    vacancy_id = response.json()["uuid"]

    response = await client.get("/v1/vacancies/get_my")
    assert response.status_code == 200
    assert len(response.json()["Vacancies"]) > 0
    assert vacancy_id in [vacancy["uuid"] for vacancy in response.json()["Vacancies"]]


@pytest.mark.asyncio
async def test_get_vacancy_by_uuid(client: AsyncClient) -> None:
    fake = Faker()
    await _create_hr_and_login(client)
    vacancy_json = {
        "title": fake.job(),
        "description": fake.text(max_nb_chars=200),
        "requirements": fake.paragraph(nb_sentences=3),
        "conditions": "free jobs",
        "salary": fake.random_int(min=30000, max=100000),
        "employment_type_str": fake.random_element(["full-time", "part-time"]),
    }
    response = await client.post(
        "/v1/vacancies/",
        json=vacancy_json,
    )
    vacancy_id = response.json()["uuid"]
    response = await client.get(f"/v1/vacancies/{vacancy_id}")
    assert response.status_code == 200
    assert response.json()["title"] == vacancy_json["title"]


@pytest.mark.asyncio
async def test_get_vacancy_by_uuid_failed_with_invalid_uuid(client: AsyncClient) -> None:
    await _create_hr_and_login(client)
    response = await client.get("/v1/vacancies/invalid_uuid")
    assert response.status_code == 422
    assert response.json()["detail"] is not None


@pytest.mark.asyncio
async def test_edit_vacancy(client: AsyncClient) -> None:
    fake = Faker()
    await _create_hr_and_login(client)
    vacancy_json = {
        "title": fake.job(),
        "description": fake.text(max_nb_chars=200),
        "requirements": fake.paragraph(nb_sentences=3),
        "conditions": "free jobs",
        "salary": fake.random_int(min=30000, max=100000),
        "employment_type_str": fake.random_element(["full-time", "part-time"]),
    }
    response = await client.post(
        "/v1/vacancies/",
        json=vacancy_json,
    )
    vacancy_id = response.json()["uuid"]

    new_description = fake.text(max_nb_chars=200)
    response = await client.patch(
        f"/v1/vacancies/edit/{vacancy_id}",
        json={"description": new_description},
    )
    assert response.status_code == 200
    assert response.json()["description"] == new_description


@pytest.mark.asyncio
async def test_edit_vacancy_failed_with_invalid_uuid(client: AsyncClient) -> None:
    await _create_hr_and_login(client)
    response = await client.patch(
        "/v1/vacancies/edit/invalid_uuid",
        json={"description": "New description"},
    )
    assert response.status_code == 422
    assert response.json()["detail"] is not None


@pytest.mark.asyncio
async def test_delete_vacancy(client: AsyncClient) -> None:
    fake = Faker()
    await _create_hr_and_login(client)
    vacancy_json = {
        "title": fake.job(),
        "description": fake.text(max_nb_chars=200),
        "requirements": fake.paragraph(nb_sentences=3),
        "conditions": "free jobs",
        "salary": fake.random_int(min=30000, max=100000),
        "employment_type_str": fake.random_element(["full-time", "part-time"]),
    }
    response = await client.post(
        "/v1/vacancies/",
        json=vacancy_json,
    )
    vacancy_id = response.json()["uuid"]
    response = await client.delete(
        f"/v1/vacancies/{vacancy_id}",
    )
    assert response.status_code == 204
    response = await client.get(f"/v1/vacancies/{vacancy_id}")
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_delete_vacancy_failed_with_invalid_uuid(client: AsyncClient) -> None:
    await _create_hr_and_login(client)
    response = await client.delete(
        "/v1/vacancies/invalid_uuid",
    )
    assert response.status_code == 422
    assert response.json()["detail"] is not None
