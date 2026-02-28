from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession

from src.dependencies import get_db
from src.shared.auth.jwt import decode_access_token
from src.shared.exceptions import UnauthorizedError

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/users/login")


async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: AsyncSession = Depends(get_db),
):
    user_id = decode_access_token(token)
    from src.users.domain.repository import UserRepository

    repo = UserRepository(db)
    user = await repo.get_by_id(user_id)
    if user is None:
        raise UnauthorizedError("User not found")
    if not user.is_active:
        raise UnauthorizedError("User account is disabled")
    return user
