from datetime import datetime
from uuid import UUID

from pydantic import BaseModel

from app.core.enums import (
    ReviewDecision,
    ReviewStatus,
)


class ReviewApproveRequest(BaseModel):
    record_id: UUID


class ReviewReturnRequest(BaseModel):
    record_id: UUID

    comments: str

    reason_for_change: str


class ReviewReopenRequest(BaseModel):
    record_id: UUID

    reason_for_change: str


class ReviewResponse(BaseModel):
    id: UUID

    record_id: UUID

    reviewer_id: UUID

    decision: ReviewDecision

    status: ReviewStatus

    comments: str | None

    reason_for_change: str | None

    created_at: datetime

    updated_at: datetime

    model_config = {
        "from_attributes": True
    }