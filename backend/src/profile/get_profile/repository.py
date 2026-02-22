from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ..models import ProfileModel


class GetProfileRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get_by_user_id(self, user_id: UUID) -> ProfileModel | None:
        result = await self._session.execute(
            select(ProfileModel).where(ProfileModel.user_id == user_id)
        )
        return result.scalar_one_or_none()
