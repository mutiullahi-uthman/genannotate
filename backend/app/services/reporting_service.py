from datetime import datetime, time, timedelta, timezone

from sqlalchemy import and_
from sqlalchemy import func

from app.models.annotation import Annotation
from app.models.dataset import Dataset
from app.models.dataset_version import DatasetVersion
from app.models.record import Record
from app.models.user import User

from app.core.enums import RecordState


class ReportingService:
    def __init__(self, db):
        self.db = db

    @staticmethod
    def _date_conditions(model, start_date, end_date):
        conditions = []

        if start_date is not None:
            start = datetime.combine(
                start_date,
                time.min,
                tzinfo=timezone.utc,
            )
            conditions.append(model.created_at >= start)

        if end_date is not None:
            end = datetime.combine(
                end_date + timedelta(days=1),
                time.min,
                tzinfo=timezone.utc,
            )
            conditions.append(model.created_at < end)

        return conditions

    def _record_count(self, start_date, end_date, state=None):
        query = self.db.query(func.count(Record.id))
        conditions = self._date_conditions(
            Record,
            start_date,
            end_date,
        )

        if state is not None:
            conditions.append(Record.state == state)

        if conditions:
            query = query.filter(*conditions)

        return query.scalar()

    def dashboard_summary(self, start_date=None, end_date=None):
        total_records = self._record_count(start_date, end_date)
        assigned_records = self._record_count(
            start_date,
            end_date,
            RecordState.ASSIGNED,
        )
        in_progress_records = self._record_count(
            start_date,
            end_date,
            RecordState.IN_PROGRESS,
        )
        submitted_records = self._record_count(
            start_date,
            end_date,
            RecordState.SUBMITTED,
        )
        approved_records = self._record_count(
            start_date,
            end_date,
            RecordState.APPROVED,
        )
        flagged_records = self._record_count(
            start_date,
            end_date,
            RecordState.FLAGGED,
        )

        return {
            "total_records": total_records,
            "assigned_records": assigned_records,
            "in_progress_records": in_progress_records,
            "submitted_records": submitted_records,
            "approved_records": approved_records,
            "flagged_records": flagged_records,
        }

    def annotator_productivity(self, start_date=None, end_date=None):
        annotation_join = and_(
            Annotation.annotator_id == User.id,
            *self._date_conditions(
                Annotation,
                start_date,
                end_date,
            ),
        )
        results = (
            self.db.query(
                User.id,
                User.full_name,
                func.count(
                    Annotation.id
                ).label("annotation_count"),
            )
            .outerjoin(
                Annotation,
                annotation_join,
            )
            .group_by(
                User.id,
                User.full_name,
            )
            .all()
        )

        return [
            {
                "user_id": row.id,
                "full_name": row.full_name,
                "annotation_count": row.annotation_count,
            }
            for row in results
        ]

    def language_breakdown(self, start_date=None, end_date=None):
        query = self.db.query(
            Record.language,
            func.count(Record.id).label("count"),
        )
        conditions = self._date_conditions(
            Record,
            start_date,
            end_date,
        )
        if conditions:
            query = query.filter(*conditions)

        results = query.group_by(Record.language).all()

        return [
            {
                "language": row.language,
                "count": row.count,
            }
            for row in results
        ]

    def dataset_summary(self, start_date=None, end_date=None):
        latest_version = (
            self.db.query(DatasetVersion.label)
            .filter(DatasetVersion.dataset_id == Dataset.id)
            .order_by(DatasetVersion.version_number.desc())
            .limit(1)
            .scalar_subquery()
        )
        record_join = and_(
            Record.dataset_id == Dataset.id,
            *self._date_conditions(
                Record,
                start_date,
                end_date,
            ),
        )
        results = (
            self.db.query(
                Dataset.id,
                Dataset.name,
                latest_version.label("version"),
                func.count(
                    Record.id
                ).label("record_count"),
            )
            .outerjoin(
                Record,
                record_join,
            )
            .group_by(
                Dataset.id,
                Dataset.name,
                latest_version,
            )
            .all()
        )

        return [
            {
                "dataset_id": row.id,
                "name": row.name,
                "version": row.version,
                "record_count": row.record_count,
            }
            for row in results
        ]