import csv
import io
import json
from datetime import datetime

from sqlalchemy.orm import Session

from app.models.annotation import Annotation
from app.models.export import Export
from app.models.record import Record

from app.core.enums import (
    ExportFormat,
    ExportStatus,
)


class ExportService:
    def __init__(self, db: Session):
        self.db = db

    def create_export_record(
        self,
        dataset_id,
        requested_by_id,
        export_format: ExportFormat,
    ):
        export = Export(
            dataset_id=dataset_id,
            requested_by_id=requested_by_id,
            export_identifier=f"EXP-{datetime.utcnow().timestamp()}",
            export_format=export_format,
            status=ExportStatus.GENERATING,
            filters={},
            record_count=0,
        )

        self.db.add(export)
        self.db.commit()
        self.db.refresh(export)

        return export

    def export_csv(
        self,
        dataset_id,
        export_record,
    ):
        annotations = (
            self.db.query(
                Annotation,
                Record,
            )
            .join(
                Record,
                Annotation.record_id == Record.id,
            )
            .filter(
                Record.dataset_id == dataset_id,
            )
            .all()
        )

        output = io.StringIO()

        writer = csv.writer(output)

        writer.writerow(
            [
                "record_id",
                "language",
                "instrument",
                "item_id",
                "construct",
                "evidence_span",
                "frequency",
                "risk_level",
                "annotation_status",
            ]
        )

        for annotation, record in annotations:
            writer.writerow(
                [
                    record.record_id,
                    record.language,
                    record.instrument,
                    record.item_id,
                    annotation.construct,
                    annotation.evidence_span,
                    annotation.frequency,
                    annotation.risk_level,
                    annotation.status,
                ]
            )

        export_record.record_count = len(
            annotations
        )

        export_record.status = (
            ExportStatus.COMPLETED
        )

        export_record.exported_at = (
            datetime.utcnow()
        )

        self.db.commit()

        return output.getvalue()

    def export_json(
        self,
        dataset_id,
        export_record,
    ):
        annotations = (
            self.db.query(
                Annotation,
                Record,
            )
            .join(
                Record,
                Annotation.record_id == Record.id,
            )
            .filter(
                Record.dataset_id == dataset_id,
            )
            .all()
        )

        results = []

        for annotation, record in annotations:
            results.append(
                {
                    "record_id": record.record_id,
                    "language": record.language,
                    "instrument": record.instrument,
                    "item_id": record.item_id,
                    "construct": annotation.construct,
                    "evidence_span": annotation.evidence_span,
                    "frequency": str(
                        annotation.frequency
                    ),
                    "risk_level": str(
                        annotation.risk_level
                    ),
                    "status": str(
                        annotation.status
                    ),
                }
            )

        export_record.record_count = len(
            annotations
        )

        export_record.status = (
            ExportStatus.COMPLETED
        )

        export_record.exported_at = (
            datetime.utcnow()
        )

        self.db.commit()

        return json.dumps(
            results,
            indent=2,
        )

    def get_export_history(
        self,
        requested_by_id=None,
    ):
        query = self.db.query(Export)
        if requested_by_id is not None:
            query = query.filter(
                Export.requested_by_id == requested_by_id
            )
        return query.order_by(Export.created_at.desc()).all()

    def get_export(
        self,
        export_id,
    ):
        return (
            self.db.query(Export)
            .filter(
                Export.id == export_id
            )
            .first()
        )
