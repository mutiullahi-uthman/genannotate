from datetime import datetime, timezone

from app.core.logging import logger
from app.tasks.celery_app import (
    celery_app,
)

from app.database.session import (
    SessionLocal,
)

from app.models.export import Export
from app.services.blob_storage_service import BlobStorageService

from app.core.enums import (
    ExportStatus,
)

from app.services.export_service import (
    ExportService,
)


@celery_app.task(
    bind=True,
    name="generate_export",
)
def generate_export(
    self,
    export_id: str,
):
    db = SessionLocal()
    export = None

    try:

        export = (
            db.query(Export)
            .filter(
                Export.id == export_id
            )
            .first()
        )

        if not export:
            logger.warning(
                "Export record not found",
                extra={"export_id": export_id},
            )
            return
        db.info["project_id"] = export.project_id

        service = ExportService(db)

        export.status = (
            ExportStatus.GENERATING
        )

        db.commit()

        if str(export.export_format) == "CSV":
            contents = service.export_csv(
                export.dataset_id,
                export,
            )
            extension = "csv"
            content_type = "text/csv; charset=utf-8"
        else:
            contents = service.export_json(
                export.dataset_id,
                export,
            )
            extension = "json"
            content_type = "application/json"

        object_key = (
            f"projects/{export.project_id}/exports/"
            f"{export.id}.{extension}"
        )
        BlobStorageService().upload_file(
            object_key=object_key,
            file_bytes=contents.encode("utf-8"),
            content_type=content_type,
        )
        export.object_key = object_key
        export.status = (
            ExportStatus.COMPLETED
        )
        export.exported_at = datetime.now(timezone.utc).isoformat()

        db.commit()

    except Exception:
        logger.exception(
            "Export job failed",
            extra={"export_id": export_id},
        )
        if export is not None:
            db.rollback()
            export = db.query(Export).filter(Export.id == export_id).first()
            if export is not None:
                db.info["project_id"] = export.project_id
                export.status = ExportStatus.FAILED
                db.commit()

        raise

    finally:
        db.close()