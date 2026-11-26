from uuid import UUID

from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from fastapi import status

from sqlalchemy.orm import Session

from app.core.auth import get_current_user
from app.core.enums import Permission
from app.core.permissions import require_permission
from app.database.session import get_db

from app.models.dataset import Dataset
from app.models.dataset_file import DatasetFile
from app.models.import_job import ImportJob

from app.core.enums import ImportJobStatus

from app.services.validation_service import (
    ValidationService,
)
from app.tasks.import_tasks import (
    process_import_job,
)

router = APIRouter(
    prefix="/imports",
    tags=["Imports"],
    dependencies=[Depends(require_permission(Permission.DATASET_CREATE))],
)

# Create a new import job for a dataset
@router.post(
    "/datasets/{dataset_id}/files/{file_id}",
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(get_current_user)],
)
def create_import_job(
    dataset_id: UUID,
    file_id: UUID,
    db: Session = Depends(get_db),
):
    dataset = (
        db.query(Dataset)
        .filter(
            Dataset.id == dataset_id
        )
        .first()
    )

    if not dataset:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Dataset not found",
        )

    dataset_file = (
        db.query(DatasetFile)
        .filter(
            DatasetFile.id == file_id
        )
        .first()
    )

    if not dataset_file:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="File not found",
        )
    if dataset_file.dataset_id != dataset_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="File not found",
        )
    if not dataset_file.upload_complete:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="File upload has not been completed.",
        )

    import_job = ImportJob(
        dataset_id=dataset_id,
        dataset_file_id=file_id,
        status=ImportJobStatus.PENDING,
    )

    db.add(import_job)
    db.commit()
    db.refresh(import_job)

    return {
        "job_id": str(import_job.id),
        "status": import_job.status,
    }
    
# Run validation on a dataset
@router.post(
    "/{job_id}/validate",
    dependencies=[Depends(get_current_user)],
)
def validate_import(
    job_id: UUID,
    db: Session = Depends(get_db),
):
    job = (
        db.query(ImportJob)
        .filter(
            ImportJob.id == job_id
        )
        .first()
    )

    if not job:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Import job not found",
        )

    if job.status in {
        ImportJobStatus.QUEUED,
        ImportJobStatus.VALIDATING,
        ImportJobStatus.IMPORTING,
        ImportJobStatus.COMPLETED,
    }:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Import job cannot be validated in its current state",
        )

    validation_service = (
        ValidationService()
    )

    validation = validation_service.validate_job(
        job=job,
        db=db,
    )

    if validation.errors:
        job.total_rows = validation.total_rows
        job.valid_rows = validation.valid_rows
        job.invalid_rows = validation.invalid_rows
        job.status = (
            ImportJobStatus.VALIDATION_FAILED
        )

        job.error_message = "\n".join(
            validation.errors
        )

        db.commit()

        return {
            "success": False,
            "errors": validation.errors,
            "total_rows": validation.total_rows,
            "valid_rows": validation.valid_rows,
            "invalid_rows": validation.invalid_rows,
        }

    job.total_rows = validation.total_rows
    job.valid_rows = validation.valid_rows
    job.invalid_rows = validation.invalid_rows
    job.status = ImportJobStatus.VALIDATED
    job.error_message = None

    db.commit()

    return {
        "success": True,
        "errors": [],
        "total_rows": validation.total_rows,
        "valid_rows": validation.valid_rows,
        "invalid_rows": validation.invalid_rows,
    }
    
# Execute the import job to import records into the dataset
@router.post(
    "/{job_id}/execute",
    dependencies=[Depends(get_current_user)],
)
def execute_import(
    job_id: UUID,
    db: Session = Depends(get_db),
):
    job = (
        db.query(ImportJob)
        .filter(
            ImportJob.id == job_id
        )
        .first()
    )

    if not job:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Import job not found",
        )

    if (
        job.status
        != ImportJobStatus.VALIDATED
    ):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=(
                "Import must be validated first"
            ),
        )

    job.status = ImportJobStatus.QUEUED
    db.commit()
    try:
        process_import_job.delay(str(job.id))
    except Exception as exc:
        job.status = ImportJobStatus.FAILED
        job.error_message = "The import worker could not be reached"
        db.commit()
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Unable to queue the import job",
        ) from exc

    return {
        "job_id": str(job.id),
        "status": "queued",
    }
    
# Get import jobs for a dataset
@router.get(
    "/datasets/{dataset_id}",
    dependencies=[Depends(get_current_user)],
)
def list_dataset_import_jobs(
    dataset_id: UUID,
    db: Session = Depends(get_db),
):
    jobs = (
        db.query(ImportJob)
        .filter(ImportJob.dataset_id == dataset_id)
        .order_by(ImportJob.created_at.desc())
        .all()
    )
    return [
        {
            "id": str(job.id),
            "status": job.status,
            "total_rows": job.total_rows,
            "valid_rows": job.valid_rows,
            "invalid_rows": job.invalid_rows,
            "error_message": job.error_message,
        }
        for job in jobs
    ]


# Get the status of an import job
@router.get(
    "/{job_id}",
    dependencies=[Depends(get_current_user)],
)
def get_import_job(
    job_id: UUID,
    db: Session = Depends(get_db),
):
    job = (
        db.query(ImportJob)
        .filter(
            ImportJob.id == job_id
        )
        .first()
    )

    if not job:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Import job not found",
        )

    return {
        "id": str(job.id),
        "status": job.status,
        "total_rows": job.total_rows,
        "valid_rows": job.valid_rows,
        "invalid_rows": job.invalid_rows,
        "error_message": job.error_message,
    }            