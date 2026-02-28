import pytest_asyncio
import src.users.domain.models  # noqa: F401
from httpx import ASGITransport, AsyncClient
from sqlalchemy import pool
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from src.config import settings
from src.dependencies import get_db
from src.main import app
from src.shared.database import Base


@pytest_asyncio.fixture
async def db_engine():
    engine = create_async_engine(settings.database_url, poolclass=pool.NullPool)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield engine
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    await engine.dispose()


@pytest_asyncio.fixture
async def db_session(db_engine):
    session_factory = async_sessionmaker(db_engine, class_=AsyncSession, expire_on_commit=False)
    async with session_factory() as session:
        yield session


@pytest_asyncio.fixture
async def client(db_session):
    async def override_get_db():
        try:
            yield db_session
            await db_session.commit()
        except Exception:
            await db_session.rollback()
            raise

    app.dependency_overrides[get_db] = override_get_db
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test",
    ) as ac:
        yield ac
    app.dependency_overrides.clear()


def user_payload():
    return {
        "email": "test@example.com",
        "password": "securepassword123",
        "full_name": "Test User",
    }


@pytest_asyncio.fixture
async def registered_user(client):
    payload = user_payload()
    response = await client.post("/api/users/register", json=payload)
    return response.json()


@pytest_asyncio.fixture
async def auth_headers(client, registered_user):
    payload = user_payload()
    response = await client.post(
        "/api/users/login",
        json={"email": payload["email"], "password": payload["password"]},
    )
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}
