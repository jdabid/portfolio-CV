---
name: github-actions
description: Creates and manages GitHub Actions CI/CD workflows for the CV Simulator platform
---

# GitHub Actions Standards

## Workflow files

All workflows live in `.github/workflows/`:

| Workflow | Trigger | Purpose |
|---|---|---|
| `ci.yml` | push main/develop, PR to main | Lint, test, build images |
| `cd-staging.yml` | push to develop | Deploy to staging environment |
| `cd-production.yml` | push to main (after CI passes) | Deploy to production |

## CI pipeline structure

Jobs run in this order:

```
lint-backend → ─┐
                 ├─→ build-images → (deploy)
test-backend → ─┘
```

- Independent jobs (lint, test) run in parallel
- `build-images` uses `needs: [lint-backend, test-backend]`
- Deploy jobs use `needs: [build-images]`

## Job conventions

- **Runner:** `ubuntu-latest`
- **Working directory:** set via `defaults.run.working-directory` per job (e.g., `backend`, `frontend`)
- **Action versions:** pin to major version (`@v4`, `@v5`)
- **Python:** `actions/setup-python@v5` with `python-version: "3.12"`
- **Node:** `actions/setup-node@v4` with `node-version: "20"` (for frontend jobs)

## Test services

Backend tests require service containers with health checks:

```yaml
services:
  postgres:
    image: postgres:16-alpine
    env:
      POSTGRES_USER: cv_user
      POSTGRES_PASSWORD: cv_password
      POSTGRES_DB: cv_simulator_test
    ports: ["5432:5432"]
    options: >-
      --health-cmd pg_isready
      --health-interval 5s
      --health-timeout 5s
      --health-retries 10

  redis:
    image: redis:7-alpine
    ports: ["6379:6379"]
    options: >-
      --health-cmd "redis-cli ping"
      --health-interval 5s
      --health-timeout 5s
      --health-retries 10
```

## Test environment variables

```yaml
env:
  POSTGRES_HOST: localhost
  POSTGRES_USER: cv_user
  POSTGRES_PASSWORD: cv_password
  POSTGRES_DB: cv_simulator_test
  REDIS_HOST: localhost
  RABBITMQ_HOST: localhost
  SECRET_KEY: test-secret-key
  DEBUG: "true"
```

## Docker image conventions

- Tag with commit SHA: `cv-simulator-api:${{ github.sha }}`
- Image names: `cv-simulator-api`, `cv-simulator-frontend`, `cv-simulator-celery`
- Registry: GitHub Container Registry (`ghcr.io/${{ github.repository }}`)

## Rules

- Never store secrets in workflow files — use GitHub Secrets (`${{ secrets.* }}`)
- All test jobs must pass before building images
- Use `continue-on-error: true` only for non-critical steps (e.g., coverage upload)
- Backend lint uses `ruff check src/ tests/`
- Backend tests use `pytest tests/ -v --cov=src --cov-report=xml`
- CD workflows must include a manual approval gate for production
- Pin third-party actions to specific versions for security
