from fastapi import APIRouter
from fastapi import Depends

from sqlalchemy.orm import Session

from app.core.auth import get_current_user
from app.core.enums import Permission
from app.core.permissions import require_permission

from app.database.session import get_db

from app.repositories.review_repository import (
    ReviewRepository,
)

from app.schemas.review import (
    ReviewApproveRequest,
    ReviewReturnRequest,
    ReviewReopenRequest,
    ReviewResponse,
)

from app.services.review_service import (
    ReviewService,
)


router = APIRouter(
    prefix="/review",
    tags=["Review"],
)

# GET /review/queue
@router.get(
    "/queue",
)
def get_review_queue(
    db: Session = Depends(get_db),
):
    service = ReviewService(
        ReviewRepository(db),
        db,
    )

    return service.get_review_queue()

# POST /review/approve
@router.post(
    "/approve",
    response_model=ReviewResponse,
    dependencies=[Depends(require_permission(Permission.REVIEW_APPROVE))],
)
def approve(
    payload: ReviewApproveRequest,
    db: Session = Depends(get_db),
    current_user=Depends(
        get_current_user
    ),
):
    service = ReviewService(
        ReviewRepository(db),
        db,
    )

    return service.approve(
        record_id=payload.record_id,
        reviewer_id=current_user.id,
    )
    
# POST /review/return
@router.post(
    "/return",
    response_model=ReviewResponse,
    dependencies=[Depends(require_permission(Permission.REVIEW_APPROVE))],
)
def return_record(
    payload: ReviewReturnRequest,
    db: Session = Depends(get_db),
    current_user=Depends(
        get_current_user
    ),
):
    service = ReviewService(
        ReviewRepository(db),
        db,
    )

    return service.return_record(
        record_id=payload.record_id,
        reviewer_id=current_user.id,
        comments=payload.comments,
        reason_for_change=payload.reason_for_change,
    )
    
# POST /review/reopen
@router.post(
    "/reopen",
    response_model=ReviewResponse,
    dependencies=[Depends(require_permission(Permission.REVIEW_APPROVE))],
)
def reopen(
    payload: ReviewReopenRequest,
    db: Session = Depends(get_db),
    current_user=Depends(
        get_current_user
    ),
):
    service = ReviewService(
        ReviewRepository(db),
        db,
    )

    return service.reopen(
        record_id=payload.record_id,
        reviewer_id=current_user.id,
        reason_for_change=payload.reason_for_change,
    )        