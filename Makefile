.PHONY: help up down build logs migrate test lint shell-api shell-db

help:
	@echo "CV Simulator — Available commands:"
	@echo ""
	@echo "  make up          Start all services (dev)"
	@echo "  make down        Stop all services"
	@echo "  make build       Rebuild all Docker images"
	@echo "  make logs        Tail logs (all services)"
	@echo "  make logs s=api  Tail logs for a specific service"
	@echo "  make migrate     Run Alembic migrations"
	@echo "  make test        Run backend tests"
	@echo "  make lint        Run ruff linter"
	@echo "  make shell-api   Open a shell in the api container"
	@echo "  make shell-db    Open psql in the postgres container"

up:
	docker compose up --build

up-d:
	docker compose up --build -d

down:
	docker compose down

build:
	docker compose build

logs:
	docker compose logs -f $(s)

migrate:
	docker compose exec api alembic upgrade head

migrate-down:
	docker compose exec api alembic downgrade -1

migrate-create:
	docker compose exec api alembic revision --autogenerate -m "$(msg)"

test:
	docker compose exec api pytest tests/ -v

lint:
	docker compose exec api ruff check src/ tests/

shell-api:
	docker compose exec api /bin/sh

shell-db:
	docker compose exec postgres psql -U cv_user -d cv_simulator
