from datetime import datetime, timezone

from sqlalchemy import func

from app.core.enums import RecordState
from app.core.logging import logger
from app.database.session import SessionLocal
from app.models.dashboard_metric import DashboardMetric
from app.models.record import Record
from app.tasks.celery_app import celery_app


@celery_app.task(name="aggregate_dashboard_metrics")
def aggregate_dashboard_metrics():
    db = SessionLocal()

    try:
        metric_date = datetime.now(timezone.utc).date()

        def count_by_state(state):
            return db.query(func.count(Record.id)).filter(
                Record.state == state
            ).scalar() or 0

        assigned = count_by_state(RecordState.ASSIGNED)
        submitted = count_by_state(RecordState.SUBMITTED)
        approved = count_by_state(RecordState.APPROVED)

        metric = db.query(DashboardMetric).filter(
            DashboardMetric.metric_date == metric_date
        ).first()

        if metric:
            metric.assigned = assigned
            metric.submitted = submitted
            metric.approved = approved
        else:
            metric = DashboardMetric(
                metric_date=metric_date,
                assigned=assigned,
                submitted=submitted,
                approved=approved,
            )
            db.add(metric)

        db.commit()

        logger.info(
            "Dashboard metrics aggregated",
            extra={"metric_date": metric_date.isoformat()},
        )

        return {
            "date": metric_date.isoformat(),
            "assigned": assigned,
            "submitted": submitted,
            "approved": approved,
        }

    except Exception:
        db.rollback()
        logger.exception("Dashboard metrics aggregation failed")
        raise

    finally:
        db.close()
