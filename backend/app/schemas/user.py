from uuid import UUID

from pydantic import BaseModel, EmailStr

from app.core.enums import UserRole
from app.core.enums import UserStatus


class MeResponse(BaseModel):
    id: UUID
    firebase_uid: str
    email: EmailStr
    full_name: str
    status: UserStatus

    model_config = {
        "from_attributes": True
    }


class ProjectUserResponse(BaseModel):
    id: UUID
    firebase_uid: str
    email: EmailStr
    full_name: str
    role: UserRole | None
    membership_active: bool | None
    status: UserStatus


class UserUpdate(BaseModel):
    role: UserRole | None = None
    membership_active: bool | None = None
    status: UserStatus | None = None