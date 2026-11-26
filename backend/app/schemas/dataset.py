from datetime import datetime
from uuid import UUID

from pydantic import BaseModel
from pydantic import Field

from app.core.enums import DatasetStatus


class DatasetCreate(BaseModel):
    name: str = Field(
        min_length=3,
        max_length=255,
    )

    language_coverage: list[str]


class DatasetUpdate(BaseModel):
    name: str | None = Field(
        default=None,
        max_length=255,
    )

    status: DatasetStatus | None = None

    language_coverage: list[str] | None = None


class DatasetVersionResponse(BaseModel):
    id: UUID
    version_number: int
    label: str
    imported_at: datetime

    model_config = {"from_attributes": True}


class DatasetResponse(BaseModel):
    id: UUID
    name: str
    status: DatasetStatus
    language_coverage: list[str]
    created_by_id: UUID
    created_at: datetime
    updated_at: datetime
    latest_version: DatasetVersionResponse | None
    versions: list[DatasetVersionResponse]

    model_config = {"from_attributes": True}