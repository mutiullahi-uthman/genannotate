from uuid import UUID

from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from fastapi import Query

from sqlalchemy.orm import Session

from app.core.auth import get_current_user
from app.core.enums import Permission, UserRole, UserStatus
from app.core.permissions import require_permission

from app.database.session import get_db
from app.models.dataset_version import DatasetVersion
from app.models.record import Record
from app.models.project import ProjectMembership
from app.models.user import User

from app.repositories.assignment_repository import (
    AssignmentRepository,
)

from app.schemas.assignment import (
    AssignmentCreate,
    AnnotatorResponse,
    AssignmentCandidateResponse,
    BulkAssignmentCreate,
    ManualBulkAssignmentCreate,
    ReassignmentRequest,
    AssignmentResponse,
)

from app.services.assignment_service import (
    AssignmentService,
)

router = APIRouter(
    prefix="/assignments",
    tags=["Assignments"],
)


@router.get(
    "/unassigned",
    response_model=list[AssignmentCandidateResponse],
    dependencies=[Depends(require_permission(Permission.RECORD_ASSIGN))],
)
def list_unassigned_records(
    dataset_id: UUID,
    dataset_version_id: UUID,
    limit: int = Query(default=500, ge=1, le=5000),
    db: Session = Depends(get_db),
):
    version = (
        db.query(DatasetVersion)
        .filter(
            DatasetVersion.id == dataset_version_id,
            DatasetVersion.dataset_id == dataset_id,
        )
        .first()
    )
    if version is None:
        raise HTTPException(
            status_code=404,
            detail="Dataset version not found",
        )

    records = (
        db.query(Record)
        .filter(
            Record.dataset_id == dataset_id,
            Record.dataset_version_id == dataset_version_id,
            Record.assignee_id.is_(None),
        )
        .order_by(Record.created_at.asc())
        .limit(limit)
        .all()
    )
    return records


@router.get(
    "/annotators",
    response_model=list[AnnotatorResponse],
    dependencies=[Depends(require_permission(Permission.RECORD_ASSIGN))],
)
def list_project_annotators(
    db: Session = Depends(get_db),
):
    return (
        db.query(User)
        .join(ProjectMembership, ProjectMembership.user_id == User.id)
        .filter(
            ProjectMembership.project_id == db.info["project_id"],
            ProjectMembership.active.is_(True),
            ProjectMembership.role == UserRole.ANNOTATOR,
            User.status == UserStatus.ACTIVE,
        )
        .order_by(User.full_name)
        .all()
    )


# Assign a record to an assignee 
@router.post(
    "",
    response_model=AssignmentResponse,
    dependencies=[Depends(require_permission(Permission.RECORD_ASSIGN))],
)
def assign_record(
    payload: AssignmentCreate,
    db: Session = Depends(get_db),
    current_user=Depends(
        get_current_user
    ),
):
    service = AssignmentService(
        AssignmentRepository(db),
        db,
    )

    return service.assign_record(
        record_id=payload.record_id,
        assignee_id=payload.assignee_id,
        assigned_by_id=current_user.id,
    )


@router.post(
    "/manual-bulk",
    dependencies=[Depends(require_permission(Permission.RECORD_ASSIGN))],
)
def manual_bulk_assign(
    payload: ManualBulkAssignmentCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    service = AssignmentService(
        AssignmentRepository(db),
        db,
    )
    assignments = service.assign_records_manually(
        record_ids=payload.record_ids,
        assignee_id=payload.assignee_id,
        assigned_by_id=current_user.id,
    )
    return {"assigned_count": len(assignments)}
    
# Bulk assign records to multiple assignees
@router.post(
    "/bulk",
    dependencies=[Depends(require_permission(Permission.RECORD_ASSIGN))],
)
def bulk_assign(
    payload: BulkAssignmentCreate,
    db: Session = Depends(get_db),
    current_user=Depends(
        get_current_user
    ),
):
    version = (
        db.query(DatasetVersion)
        .filter(
            DatasetVersion.id == payload.dataset_version_id,
            DatasetVersion.dataset_id == payload.dataset_id,
        )
        .first()
    )
    if version is None:
        raise HTTPException(
            status_code=404,
            detail="Dataset version not found",
        )

    service = AssignmentService(
        AssignmentRepository(db),
        db,
    )

    assignments = service.bulk_assign(
        dataset_id=payload.dataset_id,
        dataset_version_id=payload.dataset_version_id,
        assignee_ids=payload.assignee_ids,
        assigned_by_id=current_user.id,
        limit=payload.limit,
    )

    return {
        "assigned_count": len(assignments)
    }
    
# Reassign records to a new assignee
@router.post(
    "/reassign",
    dependencies=[Depends(require_permission(Permission.RECORD_ASSIGN))],
)
def reassign_records(
    payload: ReassignmentRequest,
    db: Session = Depends(get_db),
    current_user=Depends(
        get_current_user
    ),
):
    service = AssignmentService(
        AssignmentRepository(db),
        db,
    )

    assignments = service.reassign(
        record_ids=payload.record_ids,
        new_assignee_id=(
            payload.new_assignee_id
        ),
        assigned_by_id=current_user.id,
    )

    return {
        "reassigned_count": len(assignments)
    }        