from uuid import UUID

from pydantic import BaseModel


class UploadResponse(BaseModel):
    id: UUID

    dataset_id: UUID

    file_name: str

    blob_url: str