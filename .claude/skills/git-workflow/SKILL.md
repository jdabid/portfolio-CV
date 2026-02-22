---
name: git-workflow
description: Creates a feature branch, commits changes with conventional commits, pushes, and merges to main keeping remote branches
---

# Git Workflow Standards

## Flow
1. Run `git status` to review changes
2. Create a new branch from main with descriptive name
3. Stage and commit changes with conventional commits
4. Push branch to remote
5. Switch to main
6. Merge the feature branch into main
7. Push main to remote
8. Delete the feature branch locally only (keep remote branch)
9. Show summary of what was done

## Branch Naming Convention
<type>/<scope>-<short-description>

### Examples
- feat/profile-create-slice
- feat/profile-get-update-delete-slices
- infra/docker-setup
- test/profile-unit-tests
- ci/github-actions-pipeline
- docs/api-contract

## Commit Message Format
<type>(<scope>): <short description>

### Types
- feat: new feature or slice
- fix: bug fix
- docs: documentation only
- test: adding or updating tests
- infra: Docker, K8s, CI/CD, Helm
- refactor: code change that neither fixes nor adds
- ci: GitHub Actions or pipeline changes

## Rules
- Always start from an updated main: `git checkout main && git pull`
- One branch per logical feature/task
- Max 72 characters in commit subject
- Message in English, lowercase, no period at end
- If multiple unrelated changes exist, ask user to split into separate branches
- Never force push
- Always confirm before merging to main
- NEVER delete remote branches, only delete local branch after merge
- Show `git log --oneline -5` after merge to confirm

## Example Full Flow
```bash
git checkout main
git pull origin main
git checkout -b feat/profile-create-slice
git add .
git commit -m "feat(profile): add create_profile slice"
git push origin feat/profile-create-slice
git checkout main
git merge feat/profile-create-slice
git push origin main
git branch -d feat/profile-create-slice
```
```

Ahora después de completar cualquier tarea solo escribes:
```
> Haz commit y push de los cambios
```

Claude Code va a:

1. Crear branch → `feat/profile-create-slice`
2. Commit → `feat(profile): add create_profile slice`
3. Push del branch
4. Merge a main
5. Push main
6. Limpiar el branch local

Tu historial de Git en GitHub se va a ver así:
```
* feat(profile): add create_profile slice
* docs: add API contract and endpoint definitions
* infra: add docker-compose and dockerfiles
* initial commit