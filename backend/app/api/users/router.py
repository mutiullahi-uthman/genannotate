from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.auth import get_current_user
from app.core.enums import Permission, UserRole
from app.core.permissions import require_permission
from app.core.project_context import get_active_project_membership
from app.database.session import get_db
from app.models.project import ProjectMembership
from app.models.user import User
from app.schemas.user import ProjectUserResponse, UserUpdate

router = APIRouter(
    prefix="/users",
    tags=["Users"],
    dependencies=[Depends(require_permission(Permission.USER_MANAGE))],
)


@router.get("", response_model=list[ProjectUserResponse])
def list_users(
    db: Session = Depends(get_db),
    current_membership: ProjectMembership = Depends(
        get_active_project_membership
    ),
):
    rows = (
        db.query(User, ProjectMembership)
        .outerjoin(
            ProjectMembership,
            (ProjectMembership.user_id == User.id)
            & (
                ProjectMembership.project_id
                == current_membership.project_id
            ),
        )
        .order_by(User.created_at.desc())
        .all()
    )
    return [
        {
            "id": user.id,
            "firebase_uid": user.firebase_uid,
            "email": user.email,
            "full_name": user.full_name,
            "role": membership.role if membership else None,
            "membership_active": (
                membership.active if membership else None
            ),
            "status": user.status,
        }
        for user, membership in rows
    ]


@router.patch("/{user_id}", response_model=ProjectUserResponse)
def update_user(
    user_id: UUID,
    payload: UserUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    current_membership: ProjectMembership = Depends(
        get_active_project_membership
    ),
):
    user = (
        db.query(User)
        .filter(User.id == user_id)
        .first()
    )
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    membership = (
        db.query(ProjectMembership)
        .filter(
            ProjectMembership.project_id
            == current_membership.project_id,
            ProjectMembership.user_id == user_id,
        )
        .first()
    )
    if user.id == current_user.id and (
        (
            payload.role is not None
            and payload.role != UserRole.ADMIN
        )
        or payload.membership_active is False
    ):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="You cannot remove your own administrative access",
        )

    if payload.role is not None:
        if membership is None:
            membership = ProjectMembership(
                project_id=current_membership.project_id,
                user_id=user.id,
                role=payload.role,
                active=True,
            )
            db.add(membership)
        else:
            membership.role = payload.role

    if payload.membership_active is not None:
        if membership is None:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Assign a project role before changing membership status.",
            )
        membership.active = payload.membership_active
    if payload.status is not None:
        user.status = payload.status

    db.commit()
    return {
        "id": user.id,
        "firebase_uid": user.firebase_uid,
        "email": user.email,
        "full_name": user.full_name,
        "role": membership.role if membership else None,
        "membership_active": (
            membership.active if membership else None
        ),
        "status": user.status,
    }
