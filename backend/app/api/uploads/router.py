from pathlib import PurePosixPath
from uuid import UUID, uuid4

from fastapi import APIRouter, Depends, HTTPException, Request, status
from sqlalchemy.orm import Session

from app.core.auth import get_current_user
from app.core.enums import Permission
from app.core.permissions import require_permission
from app.core.rate_limit import limiter
from app.database.session import get_db
from app.models.dataset import Dataset
from app.models.dataset_file import DatasetFile
from app.models.user import User
from app.schemas.upload import (
    SignedUploadRequest,
    SignedUploadResponse,
    UploadCompleteRequest,
)
from app.services.blob_storage_service import BlobStorageService

router = APIRouter(
    prefix="/uploads",
    tags=["Uploads"],
    dependencies=[Depends(require_permission(Permission.DATASET_CREATE))],
)

MAX_FILE_SIZE = 50 * 1024 * 1024
ALLOWED_FILE_TYPES = {
    ".csv": {"text/csv", "application/vnd.ms-excel"},
    ".xlsx": {
        "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    },
    ".json": {"application/json"},
}


@router.post(
    "/datasets/{dataset_id}/signed-url",
    response_model=SignedUploadResponse,
    status_code=status.HTTP_201_CREATED,
)
@limiter.limit("20/minute")
def create_upload_url(
    request: Request,
    dataset_id: UUID,
    payload: SignedUploadRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    dataset = (
        db.query(Dataset)
        .filter(Dataset.id == dataset_id)
        .first()
    )
    if dataset is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Dataset not found",
        )

    file_name = payload.file_name.replace("\\", "/").rsplit("/", 1)[-1].strip()
    extension = PurePosixPath(file_name).suffix.lower()
    content_type = payload.content_type.split(";", 1)[0].strip().lower()
    if (
        not file_name
        or extension not in ALLOWED_FILE_TYPES
        or content_type not in ALLOWED_FILE_TYPES[extension]
    ):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Only CSV, XLSX, and JSON files with matching content types are supported.",
        )
    if payload.file_size > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail="File exceeds the 50MB limit.",
        )

    project_id = db.info["project_id"]
    object_key = (
        f"projects/{project_id}/datasets/{dataset_id}/"
        f"{uuid4().hex}/{file_name}"
    )
    storage = BlobStorageService()
    upload_url = storage.create_signed_upload_url(
        object_key,
        content_type,
    )

    dataset_file = DatasetFile(
        dataset_id=dataset_id,
        file_name=file_name,
        mime_type=content_type,
        file_size=payload.file_size,
        object_key=object_key,
        upload_complete=False,
        uploaded_by_id=current_user.id,
    )
    db.add(dataset_file)
    db.commit()
    db.refresh(dataset_file)

    return SignedUploadResponse(
        dataset_file_id=dataset_file.id,
        content_type=content_type,
        upload_url=upload_url,
    )


@router.post("/complete")
@limiter.limit("60/minute")
def complete_upload(
    request: Request,
    payload: UploadCompleteRequest,
    db: Session = Depends(get_db),
):
    dataset_file = (
        db.query(DatasetFile)
        .filter(DatasetFile.id == payload.dataset_file_id)
        .first()
    )
    if dataset_file is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Uploaded file not found",
        )
    if dataset_file.upload_complete:
        return {
            "id": str(dataset_file.id),
            "dataset_id": str(dataset_file.dataset_id),
            "file_name": dataset_file.file_name,
        }

    try:
        checksum = BlobStorageService().verify_uploaded_file(
            object_key=dataset_file.object_key,
            expected_size=dataset_file.file_size,
            expected_content_type=dataset_file.mime_type,
        )
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        ) from exc

    dataset_file.checksum = checksum
    dataset_file.upload_complete = True
    db.commit()

    return {
        "id": str(dataset_file.id),
        "dataset_id": str(dataset_file.dataset_id),
        "file_name": dataset_file.file_name,
    }
