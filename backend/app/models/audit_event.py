from sqlalchemy import Enum, ForeignKey, String, Text
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column

from app.core.enums import (
    AuditAction,
    AuditEntity,
)
from app.database.base import BaseModel


class AuditEvent(BaseModel):
    __tablename__ = "audit_events"

    actor_id = mapped_column(
        ForeignKey("users.id"),
        nullable=True,
    )

    entity_type: Mapped[AuditEntity] = mapped_column(
        Enum(
            AuditEntity,
            name="audit_entity",
        ),
        nullable=False,
    )

    entity_id: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
        index=True,
    )

    action: Mapped[AuditAction] = mapped_column(
        Enum(
            AuditAction,
            name="audit_action",
        ),
        nullable=False,
    )

    before_value: Mapped[dict | None] = mapped_column(
        JSONB,
        nullable=True,
    )

    after_value: Mapped[dict | None] = mapped_column(
        JSONB,
        nullable=True,
    )

    reason: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    ip_address: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
    )

    user_agent: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )
