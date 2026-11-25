from app.core.logging import logger
from app.tasks.celery_app import celery_app

from app.database.session import SessionLocal

from app.models.import_job import ImportJob

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

        imported_count = (
            import_service.import_dataset(
                import_job=job,
                db=db,
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