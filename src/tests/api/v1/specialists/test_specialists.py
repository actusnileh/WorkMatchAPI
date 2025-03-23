import pytest
from faker import Faker
from httpx import AsyncClient

from tests.utils.login import _create_user_and_login


@pytest.mark.asyncio
async def test_create_specialist(client: AsyncClient) -> None:
    faker = Faker()
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


@pytest.mark.asyncio
async def test_create_specialist_failed_with_employment_type(client: AsyncClient) -> None:
    faker = Faker()
    await _create_user_and_login(client)
    specialist_json = {
        "position": "junior",
        "about_me": faker.text(max_nb_chars=160),
        "employment_type_str": "asdasd",
    }

    response = await client.post(
        "/v1/specialist/",
        json=specialist_json,
    )

    assert response.status_code == 400


@pytest.mark.asyncio
async def test_get_specialist_by_uuid(client: AsyncClient) -> None:
    await _create_user_and_login(client)
    specialist = await client.post(
        "/v1/specialist/",
        json={
            "position": "junior",
            "about_me": "Lorem ipsum dolor sit amet, consectetur adipiscing elit.",
            "employment_type_str": "full-time",
        },
    )

    response = await client.get(
        f"/v1/specialist/{specialist.json()['uuid']}",
    )

    assert response.status_code == 200
    assert response.json()["position"] == "junior"
    assert response.json()["about_me"] == "Lorem ipsum dolor sit amet, consectetur adipiscing elit."


@pytest.mark.asyncio
async def test_get_specialist_by_uuid_failed_with_invalid_uuid(client: AsyncClient) -> None:
    await _create_user_and_login(client)
    response = await client.get(
        "/v1/specialist/invalid_uuid",
    )

    assert response.status_code == 422


@pytest.mark.asyncio
async def test_get_my_specialists(client: AsyncClient) -> None:
    await _create_user_and_login(client)
    await client.post(
        "/v1/specialist/",
        json={
            "position": "junior",
            "about_me": "Lorem ipsum dolor sit amet, consectetur adipiscing elit.",
            "employment_type_str": "full-time",
        },
    )

    response = await client.get(
        "/v1/specialist/",
    )

    assert response.status_code == 200
    assert len(response.json()["Specialists"]) > 0


@pytest.mark.asyncio
async def test_get_my_specialists_failed_without_authentication(client: AsyncClient) -> None:
    response = await client.get(
        "/v1/specialist/",
    )

    assert response.status_code == 401


@pytest.mark.asyncio
async def test_edit_specialist(client: AsyncClient) -> None:
    await _create_user_and_login(client)
    specialist = await client.post(
        "/v1/specialist/",
        json={
            "position": "junior",
            "about_me": "Lorem ipsum dolor sit amet, consectetur adipiscing elit.",
            "employment_type_str": "full-time",
        },
    )

    edit_response = await client.patch(
        f"/v1/specialist/edit/{specialist.json()['uuid']}",
        json={
            "position": "senior",
            "about_me": "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed vel lobortis neque.",
        },
    )

    assert edit_response.status_code == 200
    assert edit_response.json()["position"] == "senior"


@pytest.mark.asyncio
async def test_edit_specialist_failed_with_invalid_uuid(client: AsyncClient) -> None:
    await _create_user_and_login(client)
    response = await client.patch(
        "/v1/specialist/edit/invalid_uuid",
        json={
            "position": "senior",
            "about_me": "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed vel lobortis neque.",
        },
    )

    assert response.status_code == 422


@pytest.mark.asyncio
async def test_delete_specialist(client: AsyncClient) -> None:
    await _create_user_and_login(client)
    specialist = await client.post(
        "/v1/specialist/",
        json={
            "position": "junior",
            "about_me": "Lorem ipsum dolor sit amet, consectetur adipiscing elit.",
            "employment_type_str": "full-time",
        },
    )

    response = await client.delete(
        f"/v1/specialist/{specialist.json()['uuid']}",
    )

    assert response.status_code == 204


@pytest.mark.asyncio
async def test_delete_specialist_failed_with_invalid_uuid(client: AsyncClient) -> None:
    await _create_user_and_login(client)
    response = await client.delete(
        "/v1/specialist/invalid_uuid",
    )

    assert response.status_code == 422


@pytest.mark.asyncio
async def test_add_skill(client: AsyncClient) -> None:
    await _create_user_and_login(client)
    specialist = await client.post(
        "/v1/specialist/",
        json={
            "position": "junior",
            "about_me": "Lorem ipsum dolor sit amet, consectetur adipiscing elit.",
            "employment_type_str": "full-time",
        },
    )

    response = await client.post(
        f"/v1/specialist/{specialist.json()['uuid']}/skill",
        json={
            "skill": "python",
        },
    )

    assert response.status_code == 200
    assert "python" in response.json()["skills"]


@pytest.mark.asyncio
async def test_add_skill_failed_with_invalid_uuid(client: AsyncClient) -> None:
    await _create_user_and_login(client)
    response = await client.post(
        "/v1/specialist/invalid_uuid/skill",
        json={
            "skill": "python",
        },
    )

    assert response.status_code == 422


@pytest.mark.asyncio
async def test_delete_skill(client: AsyncClient) -> None:
    await _create_user_and_login(client)
    specialist = await client.post(
        "/v1/specialist/",
        json={
            "position": "junior",
            "about_me": "Lorem ipsum dolor sit amet, consectetur adipiscing elit.",
            "employment_type_str": "full-time",
        },
    )

    await client.post(
        f"/v1/specialist/{specialist.json()['uuid']}/skill",
        json={
            "skill": "python",
        },
    )

    response = await client.delete(
        f"/v1/specialist/{specialist.json()['uuid']}/skill/python",
    )

    assert response.status_code == 200


@pytest.mark.asyncio
async def test_delete_skill_failed_with_invalid_uuid(client: AsyncClient) -> None:
    await _create_user_and_login(client)
    response = await client.delete(
        "/v1/specialist/invalid_uuid/skill/python",
    )

    assert response.status_code == 422


@pytest.mark.asyncio
async def test_delete_skill_failed_with_nonexistent_skill(client: AsyncClient) -> None:
    await _create_user_and_login(client)
    specialist = await client.post(
        "/v1/specialist/",
        json={
            "position": "junior",
            "about_me": "Lorem ipsum dolor sit amet, consectetur adipiscing elit.",
            "employment_type_str": "full-time",
        },
    )

    response = await client.delete(
        f"/v1/specialist/{specialist.json()['uuid']}/skill/java",
    )

    assert response.status_code == 404


@pytest.mark.asyncio
async def test_add_experience(client: AsyncClient) -> None:
    await _create_user_and_login(client)
    specialist = await client.post(
        "/v1/specialist/",
        json={
            "position": "junior",
            "about_me": "Lorem ipsum dolor sit amet, consectetur adipiscing elit.",
            "employment_type_str": "full-time",
        },
    )

    response = await client.post(
        f"/v1/specialist/{specialist.json()['uuid']}/experience",
        json={
            "company_name": "ABC Corp",
            "position": "Software Engineer",
            "start_date": "2020-01-01",
            "end_date": "2021-12-31",
        },
    )

    assert response.status_code == 200
    assert "ABC Corp" in response.json()["experiences"][0]["company_name"]


@pytest.mark.asyncio
async def test_add_experience_failed_with_invalid_uuid(client: AsyncClient) -> None:
    await _create_user_and_login(client)
    response = await client.post(
        "/v1/specialist/invalid_uuid/experience",
        json={
            "company_name": "ABC Corp",
            "position": "Software Engineer",
            "start_date": "2020-01-01",
            "end_date": "2021-12-31",
        },
    )
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_delete_experience(client: AsyncClient) -> None:
    await _create_user_and_login(client)
    specialist = await client.post(
        "/v1/specialist/",
        json={
            "position": "junior",
            "about_me": "Lorem ipsum dolor sit amet, consectetur adipiscing elit.",
            "employment_type_str": "full-time",
        },
    )

    experience = await client.post(
        f"/v1/specialist/{specialist.json()['uuid']}/experience",
        json={
            "company_name": "ABC Corp",
            "position": "Software Engineer",
            "start_date": "2020-01-01",
            "end_date": "2021-12-31",
        },
    )

    experience_uuid = experience.json()["experiences"][0]["uuid"]

    response = await client.delete(
        f"/v1/specialist/{specialist.json()['uuid']}/experience/{experience_uuid}",
    )

    assert response.status_code == 200


@pytest.mark.asyncio
async def test_delete_experience_failed_with_invalid_uuid(client: AsyncClient) -> None:
    await _create_user_and_login(client)
    response = await client.delete(
        "/v1/specialist/invalid_uuid/experience/invalid_uuid",
    )

    assert response.status_code == 422


@pytest.mark.asyncio
async def test_delete_experience_failed_with_nonexistent_experience(client: AsyncClient) -> None:
    await _create_user_and_login(client)
    specialist = await client.post(
        "/v1/specialist/",
        json={
            "position": "junior",
            "about_me": "Lorem ipsum dolor sit amet, consectetur adipiscing elit.",
            "employment_type_str": "full-time",
        },
    )

    response = await client.delete(
        f"/v1/specialist/{specialist.json()['uuid']}/experience/invalid_uuid",
    )

    assert response.status_code == 422
