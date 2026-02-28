import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.config import settings
from src.shared.database import engine
from src.shared.rabbitmq import close_rabbitmq
from src.shared.rabbitmq import get_connection as get_rabbitmq
from src.shared.redis_client import close_redis, get_redis
from src.users.router import router as users_router

logger = logging.getLogger(__name__)

_services_status: dict[str, str] = {}


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    logger.info("Starting CV Simulator API...")

    # Check PostgreSQL
    try:
        async with engine.connect() as conn:
            await conn.execute(__import__("sqlalchemy").text("SELECT 1"))
        _services_status["postgres"] = "ok"
        logger.info("PostgreSQL connected")
    except Exception as e:
        _services_status["postgres"] = f"error: {e}"
        logger.warning("PostgreSQL not available: %s", e)

    # Check Redis
    try:
        redis = get_redis()
        await redis.ping()
        await redis.aclose()
        _services_status["redis"] = "ok"
        logger.info("Redis connected")
    except Exception as e:
        _services_status["redis"] = f"error: {e}"
        logger.warning("Redis not available: %s", e)

    # Check RabbitMQ
    try:
        await get_rabbitmq()
        _services_status["rabbitmq"] = "ok"
        logger.info("RabbitMQ connected")
    except Exception as e:
        _services_status["rabbitmq"] = f"error: {e}"
        logger.warning("RabbitMQ not available: %s", e)

    yield

    # Shutdown
    logger.info("Shutting down CV Simulator API...")
    await close_redis()
    await close_rabbitmq()
    await engine.dispose()


app = FastAPI(
    title="CV Simulator API",
    description="Interactive CV/portfolio platform with AI-powered features",
    version="0.1.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(users_router)


@app.get("/health", tags=["system"])
async def health_check():
    return {
        "status": "ok",
        "version": "0.1.0",
        "services": _services_status,
    }
