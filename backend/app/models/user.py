from sqlalchemy import Boolean, Enum, String
from sqlalchemy.orm import Mapped, mapped_column

from app.core.enums import UserRole, UserStatus
from app.database.base import BaseModel


class User(BaseModel):
    __tablename__ = "users"

    firebase_uid: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        nullable=False,
        index=True,
    )

    email: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        nullable=False,
        index=True,
    )

    full_name: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    role: Mapped[UserRole] = mapped_column(
        Enum(UserRole, name="user_role"),
        nullable=False,
        default=UserRole.ANNOTATOR,
    )

    status: Mapped[UserStatus] = mapped_column(
        Enum(UserStatus, name="user_status"),
        nullable=False,
        default=UserStatus.ACTIVE,
    )

    active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False,
    )