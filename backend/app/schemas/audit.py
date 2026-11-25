from datetime import datetime
from uuid import UUID

from pydantic import BaseModel

from app.core.enums import (
    AuditAction,
    AuditEntity,
)


class AuditResponse(BaseModel):
    id: UUID

    actor_id: UUID | None

    entity_type: AuditEntity

    entity_id: str

    action: AuditAction

    before_value: dict | None

    after_value: dict | None

    reason: str | None

    ip_address: str | None

    user_agent: str | None

    created_at: datetime

    model_config = {
        "from_attributes": True
    }