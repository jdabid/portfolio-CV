from fastapi import APIRouter, Depends

from src.shared.auth.dependencies import get_current_user
from src.users.domain.models import User
from src.users.get_profile.schemas import ProfileResponse

router = APIRouter()


@router.get(
    "/me",
    response_model=ProfileResponse,
    summary="Get current user profile",
    tags=["users"],
)
async def get_profile(current_user: User = Depends(get_current_user)):
    return current_user
