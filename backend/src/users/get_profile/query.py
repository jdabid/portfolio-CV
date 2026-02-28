import uuid
from dataclasses import dataclass


@dataclass(frozen=True)
class GetProfileQuery:
    user_id: uuid.UUID
