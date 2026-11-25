from fastapi import HTTPException

from app.core.enums import (
    AnnotationStatus,
    AuditAction,
    AuditEntity,
    RecordState,
)

from app.models.annotation import Annotation
from app.models.record import Record

from app.repositories.annotation_repository import (
    AnnotationRepository,
)
from app.repositories.audit_repository import (
    AuditRepository,
)
from app.services.audit_service import (
    AuditService,
)


class AnnotationService:
    def __init__(
        self,
        repository: AnnotationRepository,
        db,
    ):
        self.repository = repository
        self.db = db
        self.audit_service = AuditService(
            AuditRepository(db)
        )

    def save_draft(
        self,
        payload,
        annotator_id,
    ):
        annotation = (
            self.repository
            .get_latest_for_record(
                payload.record_id
            )
        )

        if annotation:
            annotation.is_latest = False

            revision = Annotation(
                record_id=payload.record_id,
                annotator_id=annotator_id,
                construct=payload.construct,
                evidence_span=payload.evidence_span,
                frequency=payload.frequency,
                cultural_flag=payload.cultural_flag,
                cultural_note=payload.cultural_note,
                risk_level=payload.risk_level,
                risk_rationale=payload.risk_rationale,
                status=AnnotationStatus.DRAFT,
                is_latest=True,
                version_number=annotation.version_number + 1,
                parent_annotation_id=annotation.id,
            )

            self.repository.update(annotation)
            return self.repository.create(revision)

        annotation = Annotation(
            record_id=payload.record_id,
            annotator_id=annotator_id,
            construct=payload.construct,
            evidence_span=payload.evidence_span,
            frequency=payload.frequency,
            cultural_flag=payload.cultural_flag,
            cultural_note=payload.cultural_note,
            risk_level=payload.risk_level,
            risk_rationale=payload.risk_rationale,
            status=AnnotationStatus.DRAFT,
            is_latest=True,
        )

        return self.repository.create(
            annotation
        )

    def submit_annotation(
        self,
        payload,
        annotator_id,
    ):
        annotation = self.save_draft(
            payload,
            annotator_id,
        )

        annotation.status = (
            AnnotationStatus.SUBMITTED
        )

        self.repository.update(
            annotation
        )

        record = (
            self.db.query(Record)
            .filter(
                Record.id
                == payload.record_id
            )
            .first()
        )

        if record:
            record.state = (
                RecordState.SUBMITTED
            )

            self.db.commit()

        self.audit_service.log(
            actor_id=annotator_id,
            entity_type=AuditEntity.ANNOTATION,
            entity_id=annotation.id,
            action=AuditAction.SUBMIT,
        )

        return annotation

    def get_record_annotation(
        self,
        record_id,
    ):
        return (
            self.repository
            .get_latest_for_record(
                record_id
            )
        )

    def flag_record(
        self,
        record_id,
    ):
        record = (
            self.db.query(Record)
            .filter(
                Record.id == record_id
            )
            .first()
        )

        if not record:
            raise HTTPException(
                status_code=404,
                detail="Record not found",
            )

        record.state = (
            RecordState.FLAGGED
        )

        self.db.commit()

        return {
            "status": "flagged"
        }