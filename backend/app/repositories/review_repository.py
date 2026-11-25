from uuid import UUID

from sqlalchemy.orm import Session

from app.models.review import Review
from app.models.record import Record

from app.core.enums import RecordState


class ReviewRepository:
    def __init__(
        self,
        db: Session,
    ):
        self.db = db

    def create(
        self,
        review: Review,
    ):
        self.db.add(review)
        self.db.commit()
        self.db.refresh(review)

        return review

    def get_record(
        self,
        record_id: UUID,
    ):
        return (
            self.db.query(Record)
            .filter(
                Record.id == record_id
            )
            .first()
        )

    def get_review_queue(self):
        return (
            self.db.query(Record)
            .filter(
                Record.state
                == RecordState.SUBMITTED
            )
            .all()
        )