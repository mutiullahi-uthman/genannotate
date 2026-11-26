from uuid import uuid4

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.core.auth import get_current_user
from app.core.enums import Permission, UserRole
from app.core.permissions import require_permission
from app.database.session import get_db
from app.models.project import Project, ProjectMembership
from app.models.user import User
from app.schemas.project import (
    ProjectCreate,
    ProjectMembershipResponse,
    ProjectResponse,
)


router = APIRouter(prefix="/projects", tags=["Projects"])


@router.get("/mine", response_model=list[ProjectMembershipResponse])
def list_my_projects(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    memberships = (
        db.query(ProjectMembership, Project)
        .join(Project, Project.id == ProjectMembership.project_id)
        .filter(
            ProjectMembership.user_id == current_user.id,
            ProjectMembership.active.is_(True),
            Project.active.is_(True),
        )
        .order_by(Project.name)
        .all()
    )
    return [
        {
            "id": project.id,
            "name": project.name,
            "slug": project.slug,
            "role": membership.role,
        }
        for membership, project in memberships
    ]


@router.post(
    "",
    response_model=ProjectResponse,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(require_permission(Permission.USER_MANAGE))],
)
def create_project(
    payload: ProjectCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    project = Project(
        name=payload.name.strip(),
        slug=f"project-{uuid4().hex[:16]}",
    )
    db.add(project)
    db.flush()
    db.add(
        ProjectMembership(
            project_id=project.id,
            user_id=current_user.id,
            role=UserRole.ADMIN,
            active=True,
        )
    )
    db.commit()
    db.refresh(project)
    return project
