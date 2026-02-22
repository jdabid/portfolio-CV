from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from .command import CreateProfileCommand
from .handler import CreateProfileHandler
from .schemas import CreateProfileRequest, ProfileEnvelope
from ..exceptions import ProfileAlreadyExistsError
from ...dependencies import get_current_user_id, get_db_session

router = APIRouter(tags=["profile"])


@router.post(
    "/profile",
    response_model=ProfileEnvelope,
    status_code=status.HTTP_201_CREATED,
    summary="Create profile",
    description=(
        "Creates the authenticated user's profile. "
        "Each user can have exactly one profile. "
        "Returns 409 if a profile already exists."
    ),
)
async def create_profile(
    body: CreateProfileRequest,
    user_id: UUID = Depends(get_current_user_id),
    session: AsyncSession = Depends(get_db_session),
) -> ProfileEnvelope:
    command = CreateProfileCommand(
        user_id=user_id,
        full_name=body.full_name,
        headline=body.headline,
        summary=body.summary,
        email=str(body.email),
        phone=body.phone,
        location=body.location,
        avatar_url=str(body.avatar_url) if body.avatar_url else None,
        social_links=body.social_links,
        is_public=body.is_public,
    )

    try:
        handler = CreateProfileHandler(session)
        profile = await handler.handle(command)
    except ProfileAlreadyExistsError as exc:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail={"code": "PROFILE_ALREADY_EXISTS", "message": str(exc)},
        ) from exc

    return ProfileEnvelope(data=profile)
