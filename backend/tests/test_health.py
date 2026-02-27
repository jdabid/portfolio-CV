import pytest


@pytest.mark.asyncio
async def test_health_returns_ok(client):
    response = await client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert "version" in data
    assert "services" in data


@pytest.mark.asyncio
async def test_health_returns_version(client):
    response = await client.get("/health")
    assert response.json()["version"] == "0.1.0"
