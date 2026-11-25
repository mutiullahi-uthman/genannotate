from uuid import UUID

from fastapi import APIRouter
from fastapi import Request
from fastapi import Depends
from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.core.auth import get_current_user
from app.core.rate_limit import limiter

from app.database.session import get_db

from app.core.enums import ExportFormat, Permission, UserRole
from app.core.permissions import require_permission

from app.services.export_service import (
    ExportService,
)
from app.tasks.export_tasks import (
    generate_export,
)

router = APIRouter(
    prefix="/exports",
    tags=["Exports"],
)

#CSV Export
@router.post(
    "/csv/{dataset_id}",
    dependencies=[Depends(require_permission(Permission.EXPORT_GENERATE))],
)
@limiter.limit("30/minute")
def export_csv(
    request: Request,
    dataset_id: UUID,
    db: Session = Depends(get_db),
    current_user=Depends(
        get_current_user
    ),
):
    service = ExportService(db)

    export_record = (
        service.create_export_record(
            dataset_id=dataset_id,
            requested_by_id=current_user.id,
            export_format=ExportFormat.CSV,
        )
    )

    generate_export.delay(
        str(export_record.id)
    )

    return {
        "export_id": str(export_record.id),
        "status": "queued",
    }
    
# JSON Export
@router.post(
    "/json/{dataset_id}",
    dependencies=[Depends(require_permission(Permission.EXPORT_GENERATE))],
)
@limiter.limit("30/minute")
def export_json(
    request: Request,
    dataset_id: UUID,
    db: Session = Depends(get_db),
    current_user=Depends(
        get_current_user
    ),
):
    service = ExportService(db)

    export_record = (
        service.create_export_record(
            dataset_id=dataset_id,
            requested_by_id=current_user.id,
            export_format=ExportFormat.JSON,
        )
    )

    generate_export.delay(
        str(export_record.id)
    )

    return {
        "export_id": str(export_record.id),
        "status": "queued",
    }
    
# Export History
@router.get(
    "/history",
    dependencies=[Depends(get_current_user)],
)
def export_history(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    service = ExportService(db)
    all_exports_roles = {
        UserRole.ADMIN,
        UserRole.SUPERVISOR,
        UserRole.RESEARCH_LEAD,
    }

    return service.get_export_history(
        requested_by_id=(
            None
            if current_user.role in all_exports_roles
            else current_user.id
        )
    )

# Export Details
@router.get(
    "/{export_id}",
    dependencies=[Depends(get_current_user)],
)
def get_export(
    export_id: UUID,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    service = ExportService(db)

    export = service.get_export(
        export_id
    )

    if not export:
        raise HTTPException(
            status_code=404,
            detail="Export not found",
        )

    if (
        export.requested_by_id != current_user.id
        and current_user.role
        not in {
            UserRole.ADMIN,
            UserRole.SUPERVISOR,
            UserRole.RESEARCH_LEAD,
        }
    ):
        raise HTTPException(
            status_code=404,
            detail="Export not found",
        )

    return export        