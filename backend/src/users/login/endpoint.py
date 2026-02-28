from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.dependencies import get_db
from src.users.login.command import LoginCommand
from src.users.login.handler import handle_login
from src.users.login.schemas import LoginRequest, LoginResponse

router = APIRouter()


@router.post(
    "/login",
    response_model=LoginResponse,
    summary="Login and get access token",
    tags=["users"],
)
async def login(body: LoginRequest, db: AsyncSession = Depends(get_db)):
    command = LoginCommand(email=body.email, password=body.password)
    token = await handle_login(command, db)
    return LoginResponse(access_token=token)
