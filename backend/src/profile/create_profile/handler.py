from sqlalchemy.ext.asyncio import AsyncSession

from .command import CreateProfileCommand
from .models import ProfileModel
from .repository import CreateProfileRepository
from .schemas import ProfileResponse
from ..exceptions import ProfileAlreadyExistsError


class CreateProfileHandler:
    def __init__(self, session: AsyncSession) -> None:
        self._repo = CreateProfileRepository(session)

    async def handle(self, command: CreateProfileCommand) -> ProfileResponse:
        if await self._repo.exists_for_user(command.user_id):
            raise ProfileAlreadyExistsError(command.user_id)

        profile = ProfileModel(
            user_id=command.user_id,
            full_name=command.full_name,
            headline=command.headline,
            summary=command.summary,
            email=command.email,
            phone=command.phone,
            location=command.location,
            avatar_url=str(command.avatar_url) if command.avatar_url else None,
            social_links=command.social_links.model_dump(mode="json"),
            is_public=command.is_public,
        )

        created = await self._repo.create(profile)
        return ProfileResponse.model_validate(created)
