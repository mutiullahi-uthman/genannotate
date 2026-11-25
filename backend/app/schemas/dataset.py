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

    version: str = Field(
        min_length=1,
        max_length=100,
    )

    language_coverage: list[str]


class DatasetUpdate(BaseModel):
    name: str | None = Field(
        default=None,
        max_length=255,
    )

    status: DatasetStatus | None = None

    language_coverage: list[str] | None = None


class DatasetResponse(BaseModel):
    id: UUID

    name: str
    version: str

    status: DatasetStatus

    language_coverage: list[str]

    created_by_id: UUID

    created_at: datetime
    updated_at: datetime

    model_config = {
        "from_attributes": True
    }