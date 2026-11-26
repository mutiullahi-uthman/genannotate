from sqlalchemy import func

from app.core.logging import logger
from app.tasks.celery_app import celery_app

from app.database.session import SessionLocal

from app.models.import_job import ImportJob
from app.models.dataset import Dataset
from app.models.dataset_file import DatasetFile
from app.models.dataset_version import DatasetVersion

from app.core.enums import ImportJobStatus

from app.services.import_service import (
    ImportService,
)
from app.services.import_file_service import ImportFileService

from app.services.validation_service import (
    ValidationService,
)


@celery_app.task(
    bind=True,
    name="process_import_job",
)
def process_import_job(
    self,
    import_job_id: str,
):
    db = SessionLocal()
    job = None

    try:
        job = (
            db.query(ImportJob)
            .filter(
                ImportJob.id == import_job_id
            )
            .first()
        )

        if not job:
            logger.warning(
                "Import job not found",
                extra={"import_job_id": import_job_id},
            )
            return
        db.info["project_id"] = job.project_id

        claimed = (
            db.query(ImportJob)
            .filter(
                ImportJob.id == job.id,
                ImportJob.status.in_(
                    [
                        ImportJobStatus.VALIDATED,
                        ImportJobStatus.QUEUED,
                    ]
                ),
            )
            .update(
                {
                    ImportJob.status: ImportJobStatus.VALIDATING,
                    ImportJob.error_message: None,
                },
                synchronize_session="fetch",
            )
        )
        db.commit()
        if claimed != 1:
            logger.warning(
                "Import job is not ready to process",
                extra={
                    "import_job_id": import_job_id,
                    "status": str(job.status),
                },
            )
            return

        db.refresh(job)

        validation_service = (
            ValidationService(
                ImportFileService()
            )
        )

        validation = validation_service.validate_job(
            job=job,
            db=db,
        )
        job.total_rows = validation.total_rows
        job.valid_rows = validation.valid_rows
        job.invalid_rows = validation.invalid_rows

        if validation.errors:
            job.status = (
                ImportJobStatus.VALIDATION_FAILED
            )

            job.error_message = "\n".join(
                validation.errors
            )

            db.commit()
            return

        job.status = (
            ImportJobStatus.IMPORTING
        )

        db.commit()

        if validation.parsed_file is None:
            raise RuntimeError(
                "Validated import has no parsed source file"
            )

        import_service = (
            ImportService()
        )

        dataset = (
            db.query(Dataset)
            .filter(Dataset.id == job.dataset_id)
            .with_for_update()
            .first()
        )
        dataset_file = (
            db.query(DatasetFile)
            .filter(DatasetFile.id == job.dataset_file_id)
            .first()
        )
        if dataset is None or dataset_file is None:
            raise RuntimeError(
                "Import dataset or uploaded file could not be found."
            )

        latest_version = (
            db.query(func.max(DatasetVersion.version_number))
            .filter(DatasetVersion.dataset_id == job.dataset_id)
            .scalar()
        )
        version_number = (latest_version or 0) + 1
        dataset_version = DatasetVersion(
            dataset_id=job.dataset_id,
            version_number=version_number,
            label=f"v{version_number}",
            imported_by_id=dataset_file.uploaded_by_id,
        )
        db.add(dataset_version)
        db.flush()
        job.dataset_version_id = dataset_version.id
        dataset_file.dataset_version_id = dataset_version.id

        imported_count = (
            import_service.import_dataset(
                import_job=job,
                db=db,
                dataset_version_id=dataset_version.id,
                parsed_file=validation.parsed_file,
            )
        )

        job.valid_rows = imported_count

        job.status = (
            ImportJobStatus.COMPLETED
        )

        db.commit()

    except Exception as exc:
        logger.exception(
            "Import job failed",
            extra={"import_job_id": import_job_id},
        )
        if job is not None:
            db.rollback()
            job.status = ImportJobStatus.FAILED
            job.error_message = str(exc)[:2000]
            db.commit()

        raise

    finally:
        db.close()