from datetime import date

from sqlalchemy import Date, Integer
from sqlalchemy.orm import Mapped, mapped_column

from app.database.base import BaseModel


class DashboardMetric(BaseModel):
    __tablename__ = "dashboard_metrics"

    metric_date: Mapped[date] = mapped_column(
        Date,
        nullable=False,
        unique=True,
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
