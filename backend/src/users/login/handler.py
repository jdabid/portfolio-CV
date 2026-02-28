from sqlalchemy.ext.asyncio import AsyncSession

from src.shared.auth.jwt import create_access_token
from src.shared.auth.passwords import verify_password
from src.shared.exceptions import UnauthorizedError
from src.users.domain.repository import UserRepository
from src.users.login.command import LoginCommand


async def handle_login(command: LoginCommand, db: AsyncSession) -> str:
    repo = UserRepository(db)
    user = await repo.get_by_email(command.email)
    if user is None or not verify_password(command.password, user.password_hash):
        raise UnauthorizedError("Invalid email or password")
    if not user.is_active:
        raise UnauthorizedError("User account is disabled")
    return create_access_token(user.id)
