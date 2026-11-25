from fastapi import APIRouter
from fastapi import Depends

from sqlalchemy.orm import Session

from app.core.auth import get_current_user
from app.core.enums import Permission
from app.core.permissions import require_permission

from app.database.session import get_db

from app.repositories.assignment_repository import (
    AssignmentRepository,
)

from app.schemas.assignment import (
    AssignmentCreate,
    BulkAssignmentCreate,
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
    service = AssignmentService(
        AssignmentRepository(db),
        db,
    )

    assignments = service.bulk_assign(
        dataset_id=payload.dataset_id,
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