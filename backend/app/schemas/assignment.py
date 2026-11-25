from datetime import datetime
from uuid import UUID

from pydantic import BaseModel

from app.core.enums import AssignmentType


class AssignmentCreate(BaseModel):
    record_id: UUID
    assignee_id: UUID


class BulkAssignmentCreate(BaseModel):
    dataset_id: UUID
    assignee_ids: list[UUID]
    limit: int = 100


class ReassignmentRequest(BaseModel):
    record_ids: list[UUID]
    new_assignee_id: UUID


class AssignmentResponse(BaseModel):
    id: UUID

    record_id: UUID

    old_assignee_id: UUID | None

    new_assignee_id: UUID

    assigned_by_id: UUID

    assignment_type: AssignmentType

    created_at: datetime

    model_config = {
        "from_attributes": True
    }