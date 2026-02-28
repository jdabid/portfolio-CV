import uuid
from datetime import datetime

from pydantic import BaseModel


class ProfileResponse(BaseModel):
    id: uuid.UUID
    email: str
    full_name: str
    is_active: bool
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
