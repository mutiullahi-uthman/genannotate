from datetime import date

from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from fastapi import status

from sqlalchemy.orm import Session

from app.core.enums import UserRole
from app.core.permissions import require_role
from app.database.session import get_db

from app.services.reporting_service import (
    ReportingService,
)

REPORT_ACCESS = require_role(
    UserRole.ADMIN,
    UserRole.SUPERVISOR,
    UserRole.RESEARCH_LEAD,
)


def report_date_range(
    start_date: date | None = None,
    end_date: date | None = None,
) -> tuple[date | None, date | None]:
    if start_date is not None and end_date is not None and start_date > end_date:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="start_date must be on or before end_date",
        )

    return start_date, end_date


router = APIRouter(
    prefix="/reports",
    tags=["Reports"],
    dependencies=[Depends(REPORT_ACCESS)],
)


# Dashboard Summary
@router.get(
    "/dashboard"
)
def dashboard_summary(
    db: Session = Depends(get_db),
    dates: tuple[date | None, date | None] = Depends(report_date_range),
):
    service = ReportingService(db)

    return service.dashboard_summary(*dates)

# Annotator Productivity Report
@router.get(
    "/annotators"
)
def annotator_productivity(
    db: Session = Depends(get_db),
    dates: tuple[date | None, date | None] = Depends(report_date_range),
):
    service = ReportingService(db)

    return service.annotator_productivity(*dates)

# Language Breakdown Report
@router.get(
    "/languages"
)
def language_breakdown(
    db: Session = Depends(get_db),
    dates: tuple[date | None, date | None] = Depends(report_date_range),
):
    service = ReportingService(db)

    return service.language_breakdown(*dates)

# Dataset Summary Report
@router.get(
    "/datasets"
)
def dataset_summary(
    db: Session = Depends(get_db),
    dates: tuple[date | None, date | None] = Depends(report_date_range),
):
    service = ReportingService(db)

    return service.dataset_summary(*dates)