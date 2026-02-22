from sqlalchemy.ext.asyncio import AsyncSession

from .command import DeleteProfileCommand
from .repository import DeleteProfileRepository
from ..exceptions import ProfileNotFoundError


class DeleteProfileHandler:
    def __init__(self, session: AsyncSession) -> None:
        self._repo = DeleteProfileRepository(session)

    async def handle(self, command: DeleteProfileCommand) -> None:
        profile = await self._repo.get_by_user_id(command.user_id)

        if profile is None:
            raise ProfileNotFoundError(command.user_id)

        await self._repo.delete_by_user_id(command.user_id)
