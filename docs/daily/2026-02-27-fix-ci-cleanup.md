# Fix: CI Lint Errors + Repo Cleanup

**Fecha:** 2026-02-27
**Branch:** `fix/ci-lint-and-cleanup`

---

## Problema 1: CI falló (❌ en GitHub)

### Causa raíz
El job `lint-backend` ejecuta `ruff check src/ tests/` y encontró **6 errores**:

| Error | Archivo | Regla | Descripción |
|---|---|---|---|
| 1 | `dependencies.py` | W292 | Falta newline al final del archivo |
| 2 | `main.py` | I001 | Imports desordenados |
| 3 | `rabbitmq.py` | I001 | Imports desordenados |
| 4 | `redis_client.py` | I001 | Imports desordenados |
| 5 | `worker.py` | I001 | Imports desordenados |
| 6 | `conftest.py` | I001 | Imports desordenados |

### Solución
```bash
ruff check --fix backend/src/ backend/tests/
```
Ruff auto-corrige los 6 errores: ordena imports (isort) y agrega trailing newline.

### Prevención
Correr `ruff check --fix` antes de cada commit. Se puede automatizar con:
- Un pre-commit hook (ver sección de skill/agent abajo)
- Configurar el IDE para format-on-save con ruff

---

## Problema 2: `.idea/` en el repositorio

### Causa raíz
La carpeta `.idea/` (configuración de PyCharm) fue incluida en el "first commit" inicial, **antes** de que existiera el `.gitignore`.

Aunque `.gitignore` ya tenía `.idea/` como regla, git no deja de trackear archivos que ya están en el historial.

### Solución
```bash
# 1. Eliminar del tracking (sin borrar localmente)
git rm -r --cached .idea/

# 2. Commit
git commit -m "fix: remove .idea from tracking"
```

### Prevención
- Siempre crear `.gitignore` ANTES del primer commit
- Verificar `git status` antes de hacer `git add .`

---

## Problema 3: Branch mergeada sin limpiar

### Causa raíz
Después del merge del PR, la branch `chore/complete-fase0-setup` quedó tanto local como en remoto.

### Solución
```bash
# Eliminar branch local
git branch -d chore/complete-fase0-setup

# Eliminar branch remota
git push origin --delete chore/complete-fase0-setup
```

### Prevención
- En GitHub: Settings → General → activar "Automatically delete head branches"
- Localmente: correr `git fetch --prune` periódicamente

---

## Skill/Agent para prevenir estos errores

### ¿Se puede automatizar?

**Sí.** Hay dos enfoques complementarios:

#### Opción A: Pre-commit hook (recomendado)

Un git hook que corre automáticamente antes de cada commit:

```bash
# .git/hooks/pre-commit
#!/bin/sh
ruff check --fix backend/src/ backend/tests/
ruff format backend/src/ backend/tests/
git add -u  # re-stage fixed files
```

O mejor con el framework `pre-commit`:
```yaml
# .pre-commit-config.yaml
repos:
  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.8.0
    hooks:
      - id: ruff
        args: [--fix]
      - id: ruff-format
```

#### Opción B: Claude Code hook (post-commit validation)

Claude Code soporta hooks que se ejecutan en eventos. Se puede configurar
un hook que valide lint después de cada commit.

#### Opción C: Makefile target

```makefile
pre-commit:
	ruff check --fix backend/src/ backend/tests/
	ruff format backend/src/ backend/tests/
```

### Recomendación

Implementar **pre-commit hook** (Opción A) — es el estándar de la industria y
previene que código con errores de lint llegue al repo. El CI queda como
segunda línea de defensa.
