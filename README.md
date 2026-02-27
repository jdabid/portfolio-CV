# CV Simulator

Interactive CV/portfolio platform with AI-powered features for generating, analyzing, and optimizing professional CVs.

## Stack

| Layer | Technology |
|---|---|
| Backend | FastAPI + Python 3.12 + SQLAlchemy async + Pydantic v2 |
| Frontend | React 18 + TypeScript + Vite |
| Database | PostgreSQL 16 |
| Cache | Redis 7 |
| Queue | RabbitMQ 3.13 + Celery |
| AI | Anthropic Claude API |
| Infra | Docker + Kubernetes + Helm + Kustomize |

## Architecture

- **Vertical Slice Architecture + CQRS** — each feature is a self-contained slice: `endpoint → command/query → handler → repository`
- **Async/await** everywhere in backend
- **Event-driven** communication via RabbitMQ for background processing

```
backend/src/{feature}/{action}/
  ├── endpoint.py      # FastAPI router
  ├── command.py        # Write operations (CQRS)
  ├── query.py          # Read operations (CQRS)
  ├── handler.py        # Business logic
  ├── repository.py     # Data access
  └── schemas.py        # Pydantic models
```

## Quick Start

### Prerequisites

- Docker & Docker Compose v2
- Make (optional, for shortcuts)

### Run

```bash
# Start all services
make up

# Or without Make
docker compose up --build

# Run in background
make up-d
```

### Verify

| Service | URL |
|---|---|
| API (via nginx) | http://localhost/api/health |
| API (direct) | http://localhost:8000/health |
| Frontend | http://localhost:3000 |
| RabbitMQ Management | http://localhost:15672 |

### Useful Commands

```bash
make test          # Run backend tests
make lint          # Run ruff linter
make migrate       # Run Alembic migrations
make logs          # Tail all logs
make logs s=api    # Tail specific service
make shell-api     # Shell into API container
make shell-db      # Open psql
```

## Project Structure

```
cv-simulator/
├── backend/           # FastAPI application
├── frontend/          # React SPA
├── infra/             # Docker configs, K8s manifests, Helm charts
├── docs/              # Documentation & daily progress
├── docker-compose.yml
├── docker-compose.dev.yml
├── docker-compose.prod.yml
└── Makefile
```

## Development

```bash
# Dev mode with hot reload and debug
docker compose -f docker-compose.yml -f docker-compose.dev.yml up --build
```

## License

Private — Portfolio project.
