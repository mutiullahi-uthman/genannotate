import hashlib
from pathlib import Path
from uuid import UUID
from uuid import uuid4

from fastapi import APIRouter
from fastapi import Request
from fastapi import Depends
from fastapi import File
from fastapi import HTTPException
from fastapi import UploadFile
from fastapi import status

from sqlalchemy.orm import Session

from app.core.auth import get_current_user
from app.core.rate_limit import limiter
from app.database.session import get_db

from app.models.dataset import Dataset
from app.models.dataset_file import DatasetFile
from app.models.user import User

from app.services.blob_storage_service import (
    BlobStorageService,
)

router = APIRouter(
    prefix="/uploads",
    tags=["Uploads"],
)

ALLOWED_CONTENT_TYPES = {
    "text/csv",
    "application/vnd.ms-excel",
    "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    "application/json",
}
ALLOWED_EXTENSIONS = {
    ".csv",
    ".xlsx",
    ".json",
}

MAX_FILE_SIZE = 50 * 1024 * 1024  # 50MB


@router.post(
    "/datasets/{dataset_id}",
    status_code=status.HTTP_201_CREATED,
)
@limiter.limit("20/minute")
async def upload_dataset_file(
    request: Request,
    dataset_id: UUID,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(
        get_current_user
    ),
):
    dataset = (
        db.query(Dataset)
        .filter(Dataset.id == dataset_id)
        .first()
    )

    if not dataset:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Dataset not found",
        )

    file_name = (
        (file.filename or "")
        .replace("\\", "/")
        .rsplit("/", 1)[-1]
    )
    content_type = (
        (file.content_type or "")
        .split(";", 1)[0]
        .strip()
        .lower()
    )
    extension = Path(file_name).suffix.lower()
    if (
        content_type not in ALLOWED_CONTENT_TYPES
        or extension not in ALLOWED_EXTENSIONS
    ):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=(
                "Only CSV, XLSX, and JSON files are supported"
            ),
        )

    contents = await file.read()

    if len(contents) > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="File exceeds 50MB limit",
        )

    storage = BlobStorageService()

    blob_path = (
        f"datasets/{dataset_id}/{uuid4().hex}/{file_name}"
    )

    blob_url = storage.upload_file(
        file_name=blob_path,
        file_bytes=contents,
    )

    dataset_file = DatasetFile(
        dataset_id=dataset_id,
        file_name=file_name,
        mime_type=content_type,
        file_size=len(contents),
        blob_path=blob_path,
        cdn_url=blob_url,
        checksum=hashlib.sha256(contents).hexdigest(),
        uploaded_by_id=current_user.id,
    )

    db.add(dataset_file)
    db.commit()
    db.refresh(dataset_file)

    return {
        "id": str(dataset_file.id),
        "dataset_id": str(dataset_id),
        "file_name": dataset_file.file_name,
        "blob_url": blob_url,
    }