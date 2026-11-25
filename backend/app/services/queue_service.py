from sqlalchemy import func

from app.core.enums import RecordState
from app.models.record import Record


class QueueService:
    def __init__(self, db):
        self.db = db

    def get_my_queue(
        self,
        user_id,
    ):
        return (
            self.db.query(Record)
            .filter(
                Record.assignee_id == user_id
            )
            .order_by(
                Record.created_at.asc()
            )
            .all()
        )

    def get_next_record(
        self,
        user_id,
    ):
        return (
            self.db.query(Record)
            .filter(
                Record.assignee_id == user_id,
                Record.state.in_(
                    [
                        RecordState.ASSIGNED,
                        RecordState.RETURNED,
                    ]
                ),
            )
            .order_by(
                Record.created_at.asc()
            )
            .first()
        )

    def get_queue_stats(
        self,
        user_id,
    ):
        assigned = (
            self.db.query(func.count(Record.id))
            .filter(
                Record.assignee_id == user_id,
                Record.state == RecordState.ASSIGNED,
            )
            .scalar()
        )

        in_progress = (
            self.db.query(func.count(Record.id))
            .filter(
                Record.assignee_id == user_id,
                Record.state == RecordState.IN_PROGRESS,
            )
            .scalar()
        )

        submitted = (
            self.db.query(func.count(Record.id))
            .filter(
                Record.assignee_id == user_id,
                Record.state == RecordState.SUBMITTED,
            )
            .scalar()
        )

        returned = (
            self.db.query(func.count(Record.id))
            .filter(
                Record.assignee_id == user_id,
                Record.state == RecordState.RETURNED,
            )
            .scalar()
        )

        flagged = (
            self.db.query(func.count(Record.id))
            .filter(
                Record.assignee_id == user_id,
                Record.state == RecordState.FLAGGED,
            )
            .scalar()
        )

        return {
            "assigned": assigned,
            "in_progress": in_progress,
            "submitted": submitted,
            "returned": returned,
            "flagged": flagged,
        }

    def start_annotation(
        self,
        record_id,
        user_id,
    ):
        record = (
            self.db.query(Record)
            .filter(
                Record.id == record_id,
                Record.assignee_id == user_id,
            )
            .first()
        )

        if not record:
            return None

        if record.state == RecordState.ASSIGNED:
            record.state = (
                RecordState.IN_PROGRESS
            )

            self.db.commit()
            self.db.refresh(record)

        return record