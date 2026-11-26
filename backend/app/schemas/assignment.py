from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field

from app.core.enums import AssignmentType


class AssignmentCreate(BaseModel):
    record_id: UUID
    assignee_id: UUID


class BulkAssignmentCreate(BaseModel):
    dataset_id: UUID
    dataset_version_id: UUID
    assignee_ids: list[UUID] = Field(min_length=1, max_length=100)
    limit: int = Field(default=100, ge=1, le=5000)


class ManualBulkAssignmentCreate(BaseModel):
    record_ids: list[UUID] = Field(min_length=1, max_length=500)
    assignee_id: UUID


class AssignmentCandidateResponse(BaseModel):
    id: UUID
    record_id: str
    language: str
    instrument: str
    item_id: str
    item_text: str | None

    model_config = {"from_attributes": True}


class AnnotatorResponse(BaseModel):
    id: UUID
    full_name: str
    email: str


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