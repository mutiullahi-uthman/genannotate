from uuid import UUID

from sqlalchemy.orm import Session

from app.models.assignment import Assignment
from app.models.record import Record


class AssignmentRepository:
    def __init__(
        self,
        db: Session,
    ):
        self.db = db

    def create(
        self,
        assignment: Assignment,
    ):
        self.db.add(assignment)
        self.db.commit()
        self.db.refresh(assignment)

        return assignment

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

    def get_unassigned_records(
        self,
        dataset_id: UUID,
        limit: int,
    ):
        return (
            self.db.query(Record)
            .filter(
                Record.dataset_id == dataset_id,
                Record.assignee_id.is_(None),
            )
            .limit(limit)
            .all()
        )

    def update_record(
        self,
        record: Record,
    ):
        self.db.commit()
        self.db.refresh(record)

        return record
