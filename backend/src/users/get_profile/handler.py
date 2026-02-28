from sqlalchemy.ext.asyncio import AsyncSession

from src.shared.exceptions import NotFoundError
from src.users.domain.models import User
from src.users.domain.repository import UserRepository
from src.users.get_profile.query import GetProfileQuery


async def handle_get_profile(query: GetProfileQuery, db: AsyncSession) -> User:
    repo = UserRepository(db)
    user = await repo.get_by_id(query.user_id)
    if user is None:
        raise NotFoundError("User", str(query.user_id))
    return user
