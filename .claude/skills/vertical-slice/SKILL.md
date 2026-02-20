---
name: vertical-slice
description: Generates a new feature following Vertical Slice Architecture + CQRS pattern for the CV Simulator backend
---

# Generate Vertical Slice

When creating a new feature slice, follow this exact structure:

## Directory
Create in: `backend/src/{feature_name}/{action}/`

## Files to generate

1. **schemas.py** - Pydantic v2 models for request/response
2. **command.py** - For write operations (create, update, delete)
3. **query.py** - For read operations (get, list, search)
4. **handler.py** - Business logic, receives command/query, returns result
5. **repository.py** - SQLAlchemy async operations
6. **endpoint.py** - FastAPI router, calls handler

## Rules
- Use async/await in all layers
- Commands return the created/modified entity
- Queries support pagination with limit/offset
- All schemas use Pydantic v2 model_validator where needed
- Repository uses SQLAlchemy async session
- Endpoint includes OpenAPI docs (summary, description, tags)

## Example usage
User says: "Create a slice for managing education entries"
→ Generate: backend/src/education/create_education/
→ Generate: backend/src/education/get_education/
→ Generate: backend/src/education/update_education/
→ Generate: backend/src/education/delete_education/
