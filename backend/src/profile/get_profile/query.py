from uuid import UUID

from pydantic import BaseModel


class GetProfileQuery(BaseModel):
    user_id: UUID
