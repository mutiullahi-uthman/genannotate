from uuid import UUID

from fastapi import Depends, Header, HTTPException, status
from sqlalchemy.orm import Session

from app.core.auth import get_current_user
from app.database.session import get_db
from app.models.project import Project, ProjectMembership
from app.models.user import User


def get_active_project_membership(
    project_id: UUID | None = Header(default=None, alias="X-Project-ID"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> ProjectMembership:
    if project_id is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Select an active project to continue.",
        )

    membership = (
        db.query(ProjectMembership)
        .join(Project, Project.id == ProjectMembership.project_id)
        .filter(
            ProjectMembership.project_id == project_id,
            ProjectMembership.user_id == current_user.id,
            ProjectMembership.active.is_(True),
            Project.active.is_(True),
        )
        .first()
    )
    if membership is None:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not a member of this project.",
        )

    db.info["project_id"] = membership.project_id
    return membership
