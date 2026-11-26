from uuid import UUID

from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException

from sqlalchemy.orm import Session

from app.core.auth import get_current_user
from app.core.enums import UserRole
from app.core.project_context import get_active_project_membership
from app.database.session import get_db

from app.repositories.annotation_repository import (
    AnnotationRepository,
)
from app.models.project import ProjectMembership
from app.models.record import Record
from app.models.user import User

from app.schemas.annotation import (
    AnnotationDraftRequest,
    AnnotationSubmitRequest,
    AnnotationFlagRequest,
    AnnotationResponse,
)

from app.services.annotation_service import (
    AnnotationService,
)


router = APIRouter(
    prefix="/annotations",
    tags=["Annotations"],
)

# Safe draft annotation for a record
@router.post(
    "/draft",
    response_model=AnnotationResponse,
)
def save_draft(
    payload: AnnotationDraftRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        get_current_user
    ),
    membership: ProjectMembership = Depends(
        get_active_project_membership
    ),
):
    _require_assigned_record(
        db,
        payload.record_id,
        current_user,
        membership,
    )
    service = AnnotationService(
        AnnotationRepository(db),
        db,
    )

    return service.save_draft(
        payload,
        current_user.id,
    )
    
# Submit annotation for a record
@router.post(
    "/submit",
    response_model=AnnotationResponse,
)
def submit_annotation(
    payload: AnnotationSubmitRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        get_current_user
    ),
    membership: ProjectMembership = Depends(
        get_active_project_membership
    ),
):
    _require_assigned_record(
        db,
        payload.record_id,
        current_user,
        membership,
    )
    service = AnnotationService(
        AnnotationRepository(db),
        db,
    )

    return service.submit_annotation(
        payload,
        current_user.id,
    )
    
# Flag annotation for a record
@router.post(
    "/flag"
)
def flag_record(
    payload: AnnotationFlagRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        get_current_user
    ),
    membership: ProjectMembership = Depends(
        get_active_project_membership
    ),
):
    _require_assigned_record(
        db,
        payload.record_id,
        current_user,
        membership,
    )
    service = AnnotationService(
        AnnotationRepository(db),
        db,
    )

    return service.flag_record(
        payload.record_id
    )
    
# Get the latest annotation for a record
@router.get(
    "/{record_id}",
    response_model=AnnotationResponse,
)
def get_annotation(
    record_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    membership: ProjectMembership = Depends(
        get_active_project_membership
    ),
):
    _require_assigned_record(
        db,
        record_id,
        current_user,
        membership,
    )
    service = AnnotationService(
        AnnotationRepository(db),
        db,
    )

    return service.get_record_annotation(
        record_id
    )


def _require_assigned_record(
    db: Session,
    record_id: UUID,
    current_user: User,
    membership: ProjectMembership,
) -> None:
    record = (
        db.query(Record)
        .filter(Record.id == record_id)
        .first()
    )
    if record is None or (
        membership.role == UserRole.ANNOTATOR
        and record.assignee_id != current_user.id
    ):
        raise HTTPException(
            status_code=404,
            detail="Record not found",
        )
    
                