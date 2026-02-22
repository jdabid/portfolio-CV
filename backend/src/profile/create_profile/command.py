from uuid import UUID

from pydantic import BaseModel

from .schemas import SocialLinksSchema


class CreateProfileCommand(BaseModel):
    user_id: UUID
    full_name: str
    headline: str
    summary: str | None
    email: str
    phone: str | None
    location: str | None
    avatar_url: str | None
    social_links: SocialLinksSchema
    is_public: bool
