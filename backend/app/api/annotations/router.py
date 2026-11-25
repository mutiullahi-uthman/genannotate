from uuid import UUID

from fastapi import APIRouter
from fastapi import Depends

from sqlalchemy.orm import Session

from app.core.auth import get_current_user

from app.database.session import get_db

from app.repositories.annotation_repository import (
    AnnotationRepository,
)

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
    current_user=Depends(
        get_current_user
    ),
):
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
    current_user=Depends(
        get_current_user
    ),
):
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
    current_user=Depends(
        get_current_user
    ),
):
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
):
    service = AnnotationService(
        AnnotationRepository(db),
        db,
    )

    return service.get_record_annotation(
        record_id
    )
    
                