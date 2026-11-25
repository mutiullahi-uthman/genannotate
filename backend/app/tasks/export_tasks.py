from app.core.logging import logger
from app.tasks.celery_app import (
    celery_app,
)

from app.database.session import (
    SessionLocal,
)

from app.models.export import Export

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

        service = ExportService(db)

        export.status = (
            ExportStatus.GENERATING
        )

        db.commit()

        if (
            str(export.export_format)
            == "CSV"
        ):
            service.export_csv(
                export.dataset_id,
                export,
            )
        else:
            service.export_json(
                export.dataset_id,
                export,
            )

        export.status = (
            ExportStatus.COMPLETED
        )

        db.commit()

    except Exception as exc:
        logger.exception(
            "Export job failed",
            extra={"export_id": export_id},
        )
        export.status = (
            ExportStatus.FAILED
        )

        db.commit()

        raise

    finally:
        db.close()