from sqlalchemy.ext.asyncio import AsyncSession

from src.shared.auth.passwords import hash_password
from src.shared.exceptions import ConflictError
from src.users.domain.models import User
from src.users.domain.repository import UserRepository
from src.users.register.command import RegisterUserCommand


async def handle_register(command: RegisterUserCommand, db: AsyncSession) -> User:
    repo = UserRepository(db)
    existing = await repo.get_by_email(command.email)
    if existing:
        raise ConflictError("A user with this email already exists")
    user = User(
        email=command.email,
        password_hash=hash_password(command.password),
        full_name=command.full_name,
    )
    return await repo.create(user)
