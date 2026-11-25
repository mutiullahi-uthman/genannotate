from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.auth import get_current_user
from app.core.enums import Permission, UserStatus
from app.core.permissions import require_permission
from app.database.session import get_db
from app.models.user import User
from app.schemas.user import MeResponse, UserUpdate

router = APIRouter(
    prefix="/users",
    tags=["Users"],
    dependencies=[Depends(require_permission(Permission.USER_MANAGE))],
)


@router.get("", response_model=list[MeResponse])
def list_users(db: Session = Depends(get_db)):
    return db.query(User).order_by(User.created_at.desc()).all()


@router.patch("/{user_id}", response_model=MeResponse)
def update_user(
    user_id: UUID,
    payload: UserUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    if user.id == current_user.id and (
        (
            payload.role is not None
            and payload.role != current_user.role
        )
        or (
            payload.status is not None
            and payload.status != UserStatus.ACTIVE
        )
    ):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="You cannot remove your own administrative access",
        )

    if payload.role is not None:
        user.role = payload.role
    if payload.status is not None:
        user.status = payload.status
        user.active = payload.status == UserStatus.ACTIVE

    db.commit()
    db.refresh(user)
    return user
