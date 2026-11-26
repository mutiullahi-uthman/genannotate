from datetime import datetime
from uuid import UUID

from pydantic import BaseModel

from app.core.enums import ExportFormat, ExportStatus


class ExportResponse(BaseModel):
    id: UUID
    dataset_id: UUID
    export_identifier: str
    export_format: ExportFormat
    status: ExportStatus
    record_count: int
    exported_at: str | None
    created_at: datetime

    model_config = {"from_attributes": True}
