from datetime import datetime
from uuid import UUID

from pydantic import BaseModel

from app.core.enums import (
    AnnotationStatus,
    CulturalFlag,
    FrequencyCategory,
    RiskLevel,
)


class AnnotationDraftRequest(BaseModel):
    record_id: UUID

    construct: str

    evidence_span: str

    frequency: FrequencyCategory

    cultural_flag: CulturalFlag = (
        CulturalFlag.NONE
    )

    cultural_note: str | None = None

    risk_level: RiskLevel

    risk_rationale: str | None = None


class AnnotationSubmitRequest(
    AnnotationDraftRequest
):
    pass


class AnnotationFlagRequest(BaseModel):
    record_id: UUID

    reason: str


class AnnotationResponse(BaseModel):
    id: UUID

    record_id: UUID

    annotator_id: UUID

    construct: str

    evidence_span: str

    frequency: FrequencyCategory

    cultural_flag: CulturalFlag

    cultural_note: str | None

    risk_level: RiskLevel

    risk_rationale: str | None

    status: AnnotationStatus

    created_at: datetime

    updated_at: datetime

    model_config = {
        "from_attributes": True
    }