from uuid import UUID

from pydantic import BaseModel


class DeleteProfileCommand(BaseModel):
    user_id: UUID
