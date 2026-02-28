import uuid
from datetime import UTC, datetime, timedelta

from jose import JWTError, jwt

from src.config import settings
from src.shared.exceptions import UnauthorizedError


def create_access_token(user_id: uuid.UUID) -> str:
    expire = datetime.now(UTC) + timedelta(minutes=settings.access_token_expire_minutes)
    payload = {
        "sub": str(user_id),
        "exp": expire,
        "type": "access",
    }
    return jwt.encode(payload, settings.secret_key, algorithm=settings.jwt_algorithm)


def decode_access_token(token: str) -> uuid.UUID:
    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=[settings.jwt_algorithm])
        sub = payload.get("sub")
        if sub is None:
            raise UnauthorizedError("Invalid token payload")
        return uuid.UUID(sub)
    except JWTError as err:
        raise UnauthorizedError("Could not validate credentials") from err
