from uuid import UUID

from pydantic import BaseModel, Field


class SignedUploadRequest(BaseModel):
    file_name: str = Field(min_length=1, max_length=500)
    content_type: str = Field(min_length=1, max_length=100)
    file_size: int = Field(gt=0, le=50 * 1024 * 1024)


class SignedUploadResponse(BaseModel):
    dataset_file_id: UUID
    upload_url: str
    content_type: str


class UploadCompleteRequest(BaseModel):
    dataset_file_id: UUID