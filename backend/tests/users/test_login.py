import pytest

from tests.conftest import user_payload


@pytest.mark.asyncio
async def test_login_success(client, registered_user):
    payload = user_payload()
    response = await client.post(
        "/api/users/login",
        json={"email": payload["email"], "password": payload["password"]},
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


@pytest.mark.asyncio
async def test_login_wrong_password(client, registered_user):
    payload = user_payload()
    response = await client.post(
        "/api/users/login",
        json={"email": payload["email"], "password": "wrongpassword"},
    )
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_login_nonexistent_email(client):
    response = await client.post(
        "/api/users/login",
        json={"email": "nobody@test.com", "password": "12345678"},
    )
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_login_invalid_email_format(client):
    response = await client.post(
        "/api/users/login",
        json={"email": "not-valid", "password": "12345678"},
    )
    assert response.status_code == 422
