from datetime import datetime
from uuid import UUID

from pydantic import BaseModel

from app.core.enums import ImportJobStatus


class ImportJobResponse(BaseModel):
    id: UUID

    dataset_id: UUID

    dataset_file_id: UUID

    status: ImportJobStatus

    total_rows: int

    valid_rows: int

    invalid_rows: int

    error_message: str | None

    created_at: datetime

    updated_at: datetime

    model_config = {
        "from_attributes": True
    }