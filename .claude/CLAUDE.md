# CV Simulator Platform

## What is this?
Interactive CV/portfolio application with AI-powered features.

## Architecture
- Vertical Slice Architecture + CQRS pattern
- Monorepo: backend, frontend, infra

## Stack
- Backend: FastAPI + Python 3.12 + SQLAlchemy async + Pydantic v2
- Frontend: React + TypeScript
- DB: PostgreSQL + Redis (cache)
- Queue: RabbitMQ + Celery
- Infra: Docker + Kubernetes + Helm + Kustomize

## Conventions
- Each feature is a vertical slice: endpoint → command/query → handler → repository
- Async/await everywhere in backend
- Alembic for database migrations
- pytest + httpx for testing
- All infrastructure as code in /infra

## Git Conventions
- **Commits:** Conventional Commits → `type(scope): description`
  - Types: feat, fix, refactor, chore, test, docs, ci, style, perf
  - Scopes: auth, users, cv, ai, shared, infra, ci, deps
- **Branches:** `{type}/{short-description}` (e.g., `feature/auth-login`, `fix/cv-export`)
- **Flow:** branch from main → commits → push → PR → squash merge → delete branch
- Never commit directly to main
- See `docs/git-conventions.md` for full details

## Project Structure
backend/src/{feature_name}/{action}/
  ├── endpoint.py      # FastAPI router
  ├── command.py        # Write operations (CQRS)
  ├── query.py          # Read operations (CQRS)
  ├── handler.py        # Business logic
  ├── repository.py     # Data access
  └── schemas.py        # Pydantic models
