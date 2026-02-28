import pytest


@pytest.mark.asyncio
async def test_get_profile_success(client, auth_headers):
    response = await client.get("/api/users/me", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "test@example.com"
    assert data["full_name"] == "Test User"
    assert "id" in data
    assert "created_at" in data
    assert "updated_at" in data


@pytest.mark.asyncio
async def test_get_profile_no_token(client):
    response = await client.get("/api/users/me")
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_get_profile_invalid_token(client):
    response = await client.get("/api/users/me", headers={"Authorization": "Bearer invalid-token"})
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_get_profile_malformed_header(client):
    response = await client.get("/api/users/me", headers={"Authorization": "NotBearer token"})
    assert response.status_code == 401
