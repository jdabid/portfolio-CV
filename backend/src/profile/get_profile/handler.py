from sqlalchemy.ext.asyncio import AsyncSession

from .query import GetProfileQuery
from .repository import GetProfileRepository
from ..create_profile.schemas import ProfileResponse
from ..exceptions import ProfileNotFoundError


class GetProfileHandler:
    def __init__(self, session: AsyncSession) -> None:
        self._repo = GetProfileRepository(session)

    async def handle(self, query: GetProfileQuery) -> ProfileResponse:
        profile = await self._repo.get_by_user_id(query.user_id)

        if profile is None:
            raise ProfileNotFoundError(query.user_id)

        return ProfileResponse.model_validate(profile)
