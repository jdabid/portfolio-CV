# ---- Builder stage ----
FROM python:3.12-slim AS builder

WORKDIR /build

# Create venv so all deps (including hatch's own deps like click) stay isolated
RUN python -m venv /venv
ENV PATH="/venv/bin:$PATH"

RUN pip install --upgrade pip && pip install hatch

COPY pyproject.toml .
RUN pip install --no-cache-dir .

# ---- Production stage ----
FROM python:3.12-slim AS production

WORKDIR /app

# curl for health check
RUN apt-get update && apt-get install -y --no-install-recommends curl && rm -rf /var/lib/apt/lists/*

# Non-root user
RUN addgroup --system appgroup && adduser --system --ingroup appgroup appuser

# Copy the entire venv from builder
COPY --from=builder /venv /venv
ENV PATH="/venv/bin:$PATH"

# Copy source code
COPY src/ ./src/
COPY alembic.ini .
COPY alembic/ ./alembic/

RUN chown -R appuser:appgroup /app
USER appuser

EXPOSE 8000

CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]