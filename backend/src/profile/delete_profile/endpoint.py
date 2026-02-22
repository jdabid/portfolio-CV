from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.ext.asyncio import AsyncSession

from .command import DeleteProfileCommand
from .handler import DeleteProfileHandler
from ..exceptions import ProfileNotFoundError
from ...dependencies import get_current_user_id, get_db_session

router = APIRouter(tags=["profile"])


@router.delete(
    "/profile",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete profile",
    description=(
        "Permanently deletes the authenticated user's profile. "
        "Returns 204 with no body on success. "
        "Returns 404 if no profile exists."
    ),
)
async def delete_profile(
    user_id: UUID = Depends(get_current_user_id),
    session: AsyncSession = Depends(get_db_session),
) -> Response:
    command = DeleteProfileCommand(user_id=user_id)

    try:
        handler = DeleteProfileHandler(session)
        await handler.handle(command)
    except ProfileNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"code": "PROFILE_NOT_FOUND", "message": str(exc)},
        ) from exc

    return Response(status_code=status.HTTP_204_NO_CONTENT)
