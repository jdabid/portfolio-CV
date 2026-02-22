from uuid import UUID

from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from ..models import ProfileModel


class DeleteProfileRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get_by_user_id(self, user_id: UUID) -> ProfileModel | None:
        result = await self._session.execute(
            select(ProfileModel).where(ProfileModel.user_id == user_id)
        )
        return result.scalar_one_or_none()

    async def delete_by_user_id(self, user_id: UUID) -> None:
        await self._session.execute(
            delete(ProfileModel).where(ProfileModel.user_id == user_id)
        )
        await self._session.flush()
