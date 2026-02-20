---
name: docker-setup
description: Creates and optimizes Docker and Docker Compose configurations for the CV Simulator platform
---

# Docker Configuration Standards

## Dockerfile rules
- Multi-stage builds always (builder + production)
- Base image: python:3.12-slim
- Copy requirements first for layer caching
- Non-root user in production stage
- Health checks included

## Docker Compose rules
- Services: api, frontend, postgres, redis, rabbitmq
- Named volumes for data persistence
- Custom network: cv-simulator-network
- Environment variables via .env file
- Depends_on with health checks (service_healthy)

## Ports convention
- API: 8000
- Frontend: 3000
- PostgreSQL: 5432
- Redis: 6379
- RabbitMQ: 5672 (amqp) + 15672 (management)
