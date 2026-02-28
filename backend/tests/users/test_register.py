import pytest

from tests.conftest import user_payload


@pytest.mark.asyncio
async def test_register_success(client):
    payload = user_payload()
    response = await client.post("/api/users/register", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == payload["email"]
    assert data["full_name"] == payload["full_name"]
    assert data["is_active"] is True
    assert "id" in data
    assert "created_at" in data
    assert "password_hash" not in data


@pytest.mark.asyncio
async def test_register_duplicate_email(client, registered_user):
    payload = user_payload()
    response = await client.post("/api/users/register", json=payload)
    assert response.status_code == 409


@pytest.mark.asyncio
async def test_register_invalid_email(client):
    response = await client.post(
        "/api/users/register",
        json={"email": "not-an-email", "password": "12345678", "full_name": "Test"},
    )
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_register_short_password(client):
    response = await client.post(
        "/api/users/register",
        json={"email": "test@test.com", "password": "short", "full_name": "Test"},
    )
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_register_missing_fields(client):
    response = await client.post("/api/users/register", json={"email": "test@test.com"})
    assert response.status_code == 422
