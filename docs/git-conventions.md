# Git Conventions — CV Simulator

## Branching Strategy

### Branch naming

```
{type}/{short-description}
```

| Prefijo | Uso | Ejemplo |
|---|---|---|
| `feature/` | Nueva funcionalidad | `feature/auth-login` |
| `fix/` | Corrección de bug | `fix/cv-export-crash` |
| `refactor/` | Reestructuración sin cambio de comportamiento | `refactor/base-repository` |
| `chore/` | Mantenimiento, deps, configs | `chore/update-fastapi` |
| `docs/` | Solo documentación | `docs/api-readme` |
| `test/` | Solo tests | `test/auth-integration` |
| `ci/` | Cambios en CI/CD | `ci/staging-deploy` |

### Rules

- `main` es la branch de producción — nunca se hace commit directo
- Cada feature/fix/cambio va en su propia branch
- Las branches se crean desde `main` (siempre actualizado)
- Nombres en inglés, minúsculas, separados por guiones
- Eliminar la branch después del merge

### Flow

```
1. git checkout main
2. git pull origin main
3. git checkout -b feature/auth-login
4. ... hacer commits ...
5. git push -u origin feature/auth-login
6. Crear PR → Review → Merge a main
7. git branch -d feature/auth-login
```

---

## Commit Messages

### Format: Conventional Commits

```
<type>(<scope>): <description>

[optional body]

[optional footer]
```

### Types

| Type | Cuándo usarlo |
|---|---|
| `feat` | Nueva funcionalidad para el usuario |
| `fix` | Corrección de un bug |
| `refactor` | Cambio de código que no agrega feature ni corrige bug |
| `chore` | Mantenimiento: deps, configs, scripts |
| `test` | Agregar o modificar tests |
| `docs` | Solo documentación |
| `ci` | Cambios en CI/CD (GitHub Actions, Docker) |
| `style` | Formato, linting (sin cambio de lógica) |
| `perf` | Mejora de rendimiento |

### Scopes

| Scope | Área |
|---|---|
| `auth` | Autenticación y autorización |
| `users` | Gestión de usuarios |
| `cv` | CRUD de CVs y secciones |
| `ai` | Servicio de IA |
| `shared` | Código compartido (database, exceptions, models) |
| `infra` | Docker, K8s, Helm, nginx |
| `ci` | GitHub Actions workflows |
| `deps` | Dependencias |

### Rules

- Descripción en inglés, imperativo, minúsculas, sin punto final
- Máximo 72 caracteres en la primera línea
- El scope es opcional pero recomendado
- Body para explicar el "por qué" si no es obvio

### Examples

```bash
# Features
feat(auth): add JWT login endpoint
feat(cv): add PDF export with WeasyPrint
feat(ai): add CV analysis background task

# Fixes
fix(cv): resolve null pointer on empty sections
fix(auth): handle expired refresh tokens

# Infrastructure
chore(infra): add docker-compose.dev.yml
ci: add staging deploy workflow

# Refactoring
refactor(shared): extract base repository pattern
refactor(cv): split handler into command and query

# Tests
test(auth): add login integration tests
test(cv): add create CV unit tests

# Docs
docs: add git conventions guide
docs(readme): add quick start section
```

### Breaking changes

```bash
feat(auth)!: migrate from session to JWT auth

BREAKING CHANGE: all endpoints now require Bearer token instead of session cookie.
```

---

## PR Conventions

### Title

Same format as commits: `type(scope): description`

### Body template

```markdown
## Summary
- Brief description of changes

## Changes
- List of specific changes made

## Test plan
- [ ] How to verify the changes work
```

### Merge strategy

- **Squash and merge** for feature branches (clean history on main)
- PR title becomes the squash commit message
