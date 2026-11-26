from uuid import UUID

from pydantic import BaseModel, Field

from app.core.enums import UserRole


class ProjectCreate(BaseModel):
    name: str = Field(min_length=2, max_length=255)


class ProjectMembershipResponse(BaseModel):
    id: UUID
    name: str
    slug: str
    role: UserRole


class ProjectResponse(BaseModel):
    id: UUID
    name: str
    slug: str

    model_config = {"from_attributes": True}
