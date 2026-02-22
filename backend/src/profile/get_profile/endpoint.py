from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from .handler import GetProfileHandler
from .query import GetProfileQuery
from .schemas import ProfileEnvelope
from ..exceptions import ProfileNotFoundError
from ...dependencies import get_current_user_id, get_db_session

router = APIRouter(tags=["profile"])


@router.get(
    "/profile",
    response_model=ProfileEnvelope,
    status_code=status.HTTP_200_OK,
    summary="Get profile",
    description=(
        "Returns the authenticated user's profile. "
        "Returns 404 if no profile has been created yet."
    ),
)
async def get_profile(
    user_id: UUID = Depends(get_current_user_id),
    session: AsyncSession = Depends(get_db_session),
) -> ProfileEnvelope:
    query = GetProfileQuery(user_id=user_id)

    try:
        handler = GetProfileHandler(session)
        profile = await handler.handle(query)
    except ProfileNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"code": "PROFILE_NOT_FOUND", "message": str(exc)},
        ) from exc

    return ProfileEnvelope(data=profile)
