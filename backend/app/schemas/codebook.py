from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from app.core.enums import CodebookStatus


class CodebookCreate(BaseModel):
    name: str = Field(min_length=1, max_length=255)
    version: str = Field(min_length=1, max_length=50)


class CodebookUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=255)
    version: str | None = Field(default=None, min_length=1, max_length=50)
    status: CodebookStatus | None = None


class CodebookLabelCreate(BaseModel):
    label_name: str = Field(min_length=1, max_length=255)
    definition: str = Field(min_length=1)
    inclusion_guidance: str | None = None
    exclusion_guidance: str | None = None
    examples: str | None = None


class CodebookLabelUpdate(BaseModel):
    label_name: str | None = Field(default=None, min_length=1, max_length=255)
    definition: str | None = Field(default=None, min_length=1)
    inclusion_guidance: str | None = None
    exclusion_guidance: str | None = None
    examples: str | None = None


class CodebookLabelResponse(BaseModel):
    id: UUID
    codebook_id: UUID
    label_name: str
    definition: str
    inclusion_guidance: str | None
    exclusion_guidance: str | None
    examples: str | None
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class CodebookResponse(BaseModel):
    id: UUID
    name: str
    version: str
    status: CodebookStatus
    published_by_id: UUID | None
    created_at: datetime
    updated_at: datetime
    labels: list[CodebookLabelResponse]

    model_config = ConfigDict(from_attributes=True)
