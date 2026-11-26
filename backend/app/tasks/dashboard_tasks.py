from datetime import datetime, timezone

from sqlalchemy import func

from app.core.enums import RecordState
from app.core.logging import logger
from app.database.session import SessionLocal
from app.models.dashboard_metric import DashboardMetric
from app.models.project import Project
from app.models.record import Record
from app.tasks.celery_app import celery_app


@celery_app.task(name="aggregate_dashboard_metrics")
def aggregate_dashboard_metrics():
    db = SessionLocal()

    try:
        metric_date = datetime.now(timezone.utc).date()

        project_summaries = []
        projects = db.query(Project).filter(Project.active.is_(True)).all()
        for project in projects:
            db.info["project_id"] = project.id

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
                db.add(
                    DashboardMetric(
                        project_id=project.id,
                        metric_date=metric_date,
                        assigned=assigned,
                        submitted=submitted,
                        approved=approved,
                    )
                )
            project_summaries.append(
                {
                    "project_id": str(project.id),
                    "assigned": assigned,
                    "submitted": submitted,
                    "approved": approved,
                }
            )

        db.commit()
        db.info.pop("project_id", None)

        logger.info(
            "Dashboard metrics aggregated",
            extra={
                "metric_date": metric_date.isoformat(),
                "project_count": len(project_summaries),
            },
        )

        return {
            "date": metric_date.isoformat(),
            "projects": project_summaries,
        }

    except Exception:
        db.rollback()
        logger.exception("Dashboard metrics aggregation failed")
        raise

    finally:
        db.close()
