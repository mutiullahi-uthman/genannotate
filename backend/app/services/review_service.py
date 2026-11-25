from fastapi import HTTPException

from app.core.enums import (
    AnnotationStatus,
    AuditAction,
    AuditEntity,
    RecordState,
    ReviewDecision,
    ReviewStatus,
)

from app.models.annotation import Annotation
from app.models.review import Review

from app.repositories.audit_repository import (
    AuditRepository,
)
from app.repositories.review_repository import (
    ReviewRepository,
)
from app.services.audit_service import (
    AuditService,
)


class ReviewService:
    def __init__(
        self,
        repository: ReviewRepository,
        db,
    ):
        self.repository = repository
        self.db = db
        self.audit_service = AuditService(
            AuditRepository(db)
        )

    def get_review_queue(self):
        return (
            self.repository.get_review_queue()
        )

    def approve(
        self,
        record_id,
        reviewer_id,
    ):
        record = (
            self.repository.get_record(
                record_id
            )
        )

        if not record:
            raise HTTPException(
                status_code=404,
                detail="Record not found",
            )

        record.state = (
            RecordState.APPROVED
        )

        annotation = (
            self.db.query(Annotation)
            .filter(
                Annotation.record_id
                == record_id,

                Annotation.is_latest.is_(True),
            )
            .first()
        )

        if annotation:
            annotation.status = (
                AnnotationStatus.APPROVED
            )

        review = Review(
            record_id=record_id,
            reviewer_id=reviewer_id,
            decision=ReviewDecision.APPROVE,
            status=ReviewStatus.APPROVED,
        )

        self.db.add(review)
        self.db.commit()
        self.db.refresh(review)

        self.audit_service.log(
            actor_id=reviewer_id,
            entity_type=AuditEntity.REVIEW,
            entity_id=review.id,
            action=AuditAction.APPROVE,
            after_value={
                "record_id": str(record_id),
                "decision": ReviewDecision.APPROVE.value,
            },
        )

        return review

    def return_record(
        self,
        record_id,
        reviewer_id,
        comments,
        reason_for_change,
    ):
        record = (
            self.repository.get_record(
                record_id
            )
        )

        if not record:
            raise HTTPException(
                status_code=404,
                detail="Record not found",
            )

        record.state = (
            RecordState.RETURNED
        )

        annotation = (
            self.db.query(Annotation)
            .filter(
                Annotation.record_id
                == record_id,

                Annotation.is_latest.is_(True),
            )
            .first()
        )

        if annotation:
            annotation.status = (
                AnnotationStatus.RETURNED
            )

        review = Review(
            record_id=record_id,
            reviewer_id=reviewer_id,
            decision=ReviewDecision.RETURN,
            status=ReviewStatus.RETURNED,
            comments=comments,
            reason_for_change=reason_for_change,
        )

        self.db.add(review)
        self.db.commit()
        self.db.refresh(review)

        self.audit_service.log(
            actor_id=reviewer_id,
            entity_type=AuditEntity.REVIEW,
            entity_id=review.id,
            action=AuditAction.RETURN,
            after_value={
                "record_id": str(record_id),
                "decision": ReviewDecision.RETURN.value,
            },
            reason=reason_for_change,
        )

        return review

    def reopen(
        self,
        record_id,
        reviewer_id,
        reason_for_change,
    ):
        record = (
            self.repository.get_record(
                record_id
            )
        )

        if not record:
            raise HTTPException(
                status_code=404,
                detail="Record not found",
            )

        record.state = (
            RecordState.RETURNED
        )

        review = Review(
            record_id=record_id,
            reviewer_id=reviewer_id,
            decision=ReviewDecision.REOPEN,
            status=ReviewStatus.IN_REVIEW,
            reason_for_change=reason_for_change,
        )

        self.db.add(review)
        self.db.commit()
        self.db.refresh(review)

        self.audit_service.log(
            actor_id=reviewer_id,
            entity_type=AuditEntity.REVIEW,
            entity_id=review.id,
            action=AuditAction.REOPEN,
            after_value={
                "record_id": str(record_id),
                "decision": ReviewDecision.REOPEN.value,
            },
            reason=reason_for_change,
        )

        return review