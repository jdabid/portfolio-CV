from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.dependencies import get_db
from src.users.register.command import RegisterUserCommand
from src.users.register.handler import handle_register
from src.users.register.schemas import RegisterRequest, RegisterResponse

router = APIRouter()


@router.post(
    "/register",
    response_model=RegisterResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Register a new user",
    tags=["users"],
)
async def register(body: RegisterRequest, db: AsyncSession = Depends(get_db)):
    command = RegisterUserCommand(
        email=body.email, password=body.password, full_name=body.full_name
    )
    user = await handle_register(command, db)
    return user
