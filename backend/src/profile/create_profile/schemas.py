from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, EmailStr, Field, HttpUrl, model_validator


class SocialLinksSchema(BaseModel):
    model_config = ConfigDict(extra="forbid")

    linkedin: HttpUrl | None = None
    github: HttpUrl | None = None
    website: HttpUrl | None = None
    twitter: HttpUrl | None = None


class CreateProfileRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    full_name: str = Field(..., min_length=2, max_length=120)
    headline: str = Field(..., min_length=5, max_length=220)
    summary: str | None = Field(None, max_length=2000)
    email: EmailStr
    phone: str | None = Field(None, pattern=r"^\+?[\d\s\-()\d]{7,20}$")
    location: str | None = Field(None, max_length=120)
    avatar_url: HttpUrl | None = None
    social_links: SocialLinksSchema = Field(default_factory=SocialLinksSchema)
    is_public: bool = False


class ProfileResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
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
    created_at: datetime
    updated_at: datetime


class ProfileEnvelope(BaseModel):
    data: ProfileResponse
