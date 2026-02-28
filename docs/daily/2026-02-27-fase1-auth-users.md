# Fase 1 — Auth + Users

**Fecha:** 2026-02-27
**Branch:** `feature/auth-users`
**Duración estimada:** 25h | **Real esta sesión:** ~4h

---

## Entregables completados

| Entregable | Estado |
|---|---|
| Registro de usuario (POST /api/users/register) | Done |
| Login con JWT (POST /api/users/login) | Done |
| Perfil protegido (GET /api/users/me) | Done |
| Migración Alembic (tabla users) | Done |
| Tests (15 passed) | Done |

## Endpoints implementados

| Method | Path | Auth | Response |
|---|---|---|---|
| POST | `/api/users/register` | No | 201 + user data |
| POST | `/api/users/login` | No | 200 + JWT token |
| GET | `/api/users/me` | Bearer JWT | 200 + profile |

## Arquitectura aplicada

```
backend/src/
├── shared/auth/           # JWT + password utils + get_current_user dependency
├── users/
│   ├── domain/            # User model (BaseEntity) + UserRepository
│   ├── register/          # Vertical Slice: endpoint → command → handler → schemas
│   ├── login/             # Vertical Slice: endpoint → command → handler → schemas
│   ├── get_profile/       # Vertical Slice: endpoint → query → handler → schemas
│   └── router.py          # Aggregates slices → /api/users
```

## Decisiones técnicas

| Decisión | Elección | Razón |
|---|---|---|
| JWT | Access token only (60 min) | Simple para portfolio, refresh se puede agregar después |
| Password | bcrypt directo | passlib incompatible con bcrypt >= 4.1 (unmaintained) |
| Repository | Compartido por feature | Evita duplicar get_by_email/get_by_id |
| Test engine | NullPool per-fixture | Evita conflictos de event loop entre tests |

## Tests

```
tests/test_health.py          2 passed
tests/users/test_register.py  5 passed
tests/users/test_login.py     4 passed
tests/users/test_get_profile.py 4 passed
Total: 15 passed in 3.23s
```

## Bugs encontrados y resueltos

Ver `docs/bugs/2026-02-27-fase1-bugs.md` para detalles completos.
