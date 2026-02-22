from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from .models import ProfileModel


class CreateProfileRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def exists_for_user(self, user_id: UUID) -> bool:
        result = await self._session.execute(
            select(ProfileModel.id).where(ProfileModel.user_id == user_id)
        )
        return result.scalar_one_or_none() is not None

    async def create(self, profile: ProfileModel) -> ProfileModel:
        self._session.add(profile)
        await self._session.flush()
        await self._session.refresh(profile)
        return profile
