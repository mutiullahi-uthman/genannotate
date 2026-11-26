from datetime import date

from sqlalchemy import Date, Integer, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from app.database.base import BaseModel, ProjectScopedMixin


class DashboardMetric(ProjectScopedMixin, BaseModel):
    __tablename__ = "dashboard_metrics"
    __table_args__ = (
        UniqueConstraint(
            "project_id",
            "metric_date",
            name="uq_dashboard_metrics_project_date",
        ),
    )

    metric_date: Mapped[date] = mapped_column(
        Date,
        nullable=False,
        index=True,
    )

    assigned: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=0,
    )

    submitted: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=0,
    )

    approved: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=0,
    )
