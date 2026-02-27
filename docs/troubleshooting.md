# Troubleshooting Guide — CV Simulator

Registro de bugs encontrados durante el setup y desarrollo, con causa raíz, solución y comandos exactos.

---

## BUG-001 — `.env` file not found

**Fecha:** 2026-02-27
**Contexto:** Primera ejecución de `make up`

### Error
```
env file /path/to/portfolio-CV/.env not found: stat .env: no such file or directory
make: *** [up] Error 1
```

### Causa
Docker Compose requiere un archivo `.env` en la raíz del proyecto. El repo solo incluye `.env.example` por seguridad (nunca se commitea el `.env` real).

### Solución
```bash
cp .env.example .env
```

### Notas
- Edita `.env` antes de levantar si necesitas claves reales (ej. `ANTHROPIC_API_KEY`)
- Genera un `SECRET_KEY` seguro con: `openssl rand -hex 32`
- El `.gitignore` excluye `.env` por diseño — nunca lo commitees

---

## BUG-002 — Docker daemon I/O error (`containerdmeta.db`)

**Fecha:** 2026-02-27
**Contexto:** Primera ejecución después de instalar Docker Desktop

### Error
```
Error response from daemon: error creating temporary lease:
write /var/lib/desktop-containerd/daemon/io.containerd.metadata.v1.bolt/meta.db:
input/output error: unknown
make: *** [up] Error 18
```

### Causa
La base de datos interna de containerd (`meta.db`) de Docker Desktop se corrompió — ocurre frecuentemente en la primera ejecución o después de apagados bruscos.

### Solución paso a paso

**Opción A — Reinicio simple (intenta primero):**
```bash
# Cerrar y reiniciar Docker Desktop
pkill -f "Docker Desktop"
sleep 5
open -a "Docker Desktop"
# Espera ~30 segundos y vuelve a ejecutar make up
```

**Opción B — Limpiar datos corruptos (si A falla):**
```bash
# ADVERTENCIA: elimina imágenes locales (no afecta tu código)
pkill -f "Docker Desktop"
rm -rf ~/Library/Containers/com.docker.docker/Data/vms/0/data/
open -a "Docker Desktop"
# Espera que inicialice (~60s) y ejecuta make up
```

**Opción C — Factory Reset desde UI:**
1. Docker Desktop → Settings (engranaje)
2. Troubleshoot → "Clean / Purge data"
3. Confirmar y esperar reinicio

### Verificación
```bash
docker info | head -3
# Debe mostrar "Server Version: XX.XX"
```

---

## BUG-003 — Frontend `/build/dist` not found en Docker

**Fecha:** 2026-02-27
**Contexto:** Build del contenedor `frontend`

### Error
```
[frontend production 2/3] COPY --from=builder /build/dist /usr/share/nginx/html
ERROR: failed to calculate checksum of ref ...: "/build/dist": not found
```

### Causa
Dos problemas combinados:
1. El `Dockerfile` original copiaba solo `package.json` sin `package-lock.json`
2. Sin lock file, Docker usó una capa cacheada corrupta del primer intento fallido (cuando el daemon se cayó). `npm install` corría en 0.1s (imposible sin cache), dejando `node_modules` vacío sin que Docker lo detectara como error

### Solución

**Paso 1 — Generar `package-lock.json` localmente:**
```bash
cd frontend
npm install   # crea package-lock.json
```

**Paso 2 — Corregir el Dockerfile:**

Archivo: `frontend/Dockerfile`

```dockerfile
# ANTES (buggy)
COPY package.json .
RUN npm install

# DESPUÉS (correcto)
COPY package.json package-lock.json ./
RUN npm ci
```

**Paso 3 — Rebuild sin cache:**
```bash
docker compose build --no-cache frontend
```

### Por qué `npm ci` en vez de `npm install`
- `npm ci` requiere `package-lock.json` y falla si no existe → falla explícita, no silenciosa
- Instalación determinista y reproducible
- Más rápido en CI/CD (no resuelve versiones)

---

## BUG-004 — `ModuleNotFoundError: No module named 'click'` en API

**Fecha:** 2026-02-27
**Contexto:** Startup del contenedor `api`

### Error
```
File "/usr/local/bin/uvicorn", line 3, in <module>
    from uvicorn.main import main
  File "/usr/local/lib/python3.12/site-packages/uvicorn/__init__.py"
    from uvicorn.config import Config
  File ".../uvicorn/config.py", line 17, in <module>
    import click
ModuleNotFoundError: No module named 'click'
```

### Causa
El Dockerfile original usaba `pip install --prefix=/install .` en el builder stage. El problema:

1. `hatch` se instala **globalmente** en el builder (`pip install hatch`)
2. `hatch` depende de `click` → `click` queda en el Python global del builder
3. `pip install --prefix=/install .` ve que `click` ya está instalado globalmente → **no lo instala en `/install`**
4. El production stage copia solo `/install` → `click` nunca llega al contenedor final

### Solución — Usar virtual environment en el builder

Archivo: `backend/Dockerfile`

```dockerfile
# ANTES (buggy — --prefix tiene conflictos con packages globales)
FROM python:3.12-slim AS builder
WORKDIR /build
RUN pip install --upgrade pip && pip install hatch
COPY pyproject.toml .
RUN pip install --no-cache-dir --prefix=/install .

FROM python:3.12-slim AS production
COPY --from=builder /install /usr/local

# DESPUÉS (correcto — venv aísla todo)
FROM python:3.12-slim AS builder
WORKDIR /build
RUN python -m venv /venv
ENV PATH="/venv/bin:$PATH"
RUN pip install --upgrade pip && pip install hatch
COPY pyproject.toml .
RUN pip install --no-cache-dir .

FROM python:3.12-slim AS production
COPY --from=builder /venv /venv
ENV PATH="/venv/bin:$PATH"
```

### Verificación
```bash
docker run --rm --entrypoint python cv-simulator-api \
  -c "import click, uvicorn, fastapi; print('OK')"
```

### Regla general
Nunca usar `pip install --prefix` en multi-stage builds si hay herramientas instaladas globalmente en el builder. Siempre usar `python -m venv`.

---

## BUG-005 — `pydantic_settings.exceptions.SettingsError` en `allowed_origins`

**Fecha:** 2026-02-27
**Contexto:** Startup del contenedor `api` (después de resolver BUG-004)

### Error
```
pydantic_settings.exceptions.SettingsError: error parsing value for field
"allowed_origins" from source "EnvSettingsSource"

json.decoder.JSONDecodeError: Expecting value: line 1 column 1 (char 0)
```

### Causa
En pydantic-settings v2, los campos de tipo `list[str]` se parsean desde variables de entorno en formato **JSON**, no CSV. El `.env` tenía:

```
# ANTES (CSV — no válido para pydantic-settings v2)
ALLOWED_ORIGINS=http://localhost:3000,http://localhost:80
```

Pydantic-settings intenta `json.loads("http://localhost:3000,http://localhost:80")` → falla.

### Solución

Archivo: `.env` y `.env.example`

```bash
# DESPUÉS (JSON — correcto para pydantic-settings v2)
ALLOWED_ORIGINS=["http://localhost:3000","http://localhost:80"]
```

### Regla general
En pydantic-settings v2, todos los campos de tipo `list`, `dict`, o tipos complejos en `.env` deben estar en formato JSON válido.

---

## BUG-006 — API container `unhealthy` (health check falla)

**Fecha:** 2026-02-27
**Contexto:** `docker compose up -d` — api queda en estado `unhealthy`

### Error
```
Container cv-simulator-api-1  Error
dependency failed to start: container cv-simulator-api-1 is unhealthy
```

### Causa
El health check en `docker-compose.yml` usa `curl`:
```yaml
healthcheck:
  test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
```

La imagen `python:3.12-slim` **no incluye `curl`** por defecto. El health check siempre fallaba aunque la API estuviera corriendo correctamente.

### Solución

Archivo: `backend/Dockerfile` (production stage)

```dockerfile
# Agregar antes de crear el usuario no-root
RUN apt-get update && apt-get install -y --no-install-recommends curl \
    && rm -rf /var/lib/apt/lists/*
```

```bash
# Rebuild y levantar
docker compose build api
docker compose up -d
```

### Verificación
```bash
docker compose ps
# api debe mostrar: Up X seconds (healthy)

curl http://localhost:8000/health
# {"status":"ok","version":"0.1.0","services":{"postgres":"ok","redis":"ok","rabbitmq":"ok"}}
```

---

## Estado final del stack

```
SERVICE       PORT    STATUS
api           8000    healthy ✓
frontend      3000    running ✓
nginx         80      running ✓
postgres      5432    healthy ✓
redis         6379    healthy ✓
rabbitmq      5672    healthy ✓
rabbitmq-ui   15672   running ✓
celery-worker —       running ✓
```

---

## Skills y Agents para bugs futuros

### Skills disponibles en este proyecto

| Skill | Cuándo usarlo |
|---|---|
| `docker-setup` | Dockerfile buggy, multi-stage build issues, docker-compose mal configurado, optimización de capas |
| `vertical-slice` | Crear un nuevo feature (endpoint + CQRS + handler + repository) siguiendo la arquitectura del proyecto |
| `ai-feature` | Implementar features que usen LLMs / Anthropic API |
| `k8s-deploy` | Problemas con manifests de Kubernetes, Helm charts, Kustomize overlays |

### Cómo invocar un skill
```
# En el chat con Claude Code:
/docker-setup    → para problemas de Docker/Dockerfile
/vertical-slice  → para crear un nuevo feature
/ai-feature      → para features con IA
/k8s-deploy      → para infraestructura Kubernetes
```

### Agents de Claude Code para debugging

| Tipo de bug | Agent recomendado | Ejemplo de prompt |
|---|---|---|
| Bug de código complejo, causa desconocida | `general-purpose` | "Investiga por qué el handler de auth falla con JWT expirado" |
| Buscar dónde está algo en el codebase | `Explore` | "Encuentra todos los endpoints que no tienen autenticación" |
| Planear refactor o feature grande | `Plan` | "Diseña el sistema de auth con JWT para FastAPI" |
| Preguntas sobre Claude Code / API | `claude-code-guide` | "Cómo configuro hooks para formatear código antes de commit" |

### Guía rápida: ¿qué usar para qué bug?

```
¿Error en Dockerfile o docker-compose?
  → Skill: docker-setup

¿Error de Python en el backend (imports, config, SQLAlchemy)?
  → Agent: general-purpose + lee los logs con: docker compose logs api

¿Error de TypeScript/React en el frontend?
  → Agent: general-purpose + lee los logs con: docker compose logs frontend

¿Quieres agregar un nuevo endpoint?
  → Skill: vertical-slice

¿Problema de infraestructura (K8s, Helm)?
  → Skill: k8s-deploy

¿No sabes dónde está el código relevante?
  → Agent: Explore (thoroughness: "medium")

¿Quieres planear una feature compleja antes de implementar?
  → Agent: Plan
```

---

## Comandos de diagnóstico rápido

```bash
# Ver estado de todos los servicios
docker compose ps

# Ver logs de un servicio específico
docker compose logs api --tail=50
docker compose logs celery-worker --tail=50

# Reiniciar un servicio sin bajar todo el stack
docker compose restart api

# Entrar al contenedor de la API
docker compose exec api bash

# Verificar salud del sistema
curl http://localhost:8000/health

# Ver uso de recursos
docker stats --no-stream
```