from fastapi import Depends
from fastapi import HTTPException
from fastapi import status

from app.core.auth import get_current_user
from app.core.enums import Permission, UserRole
from app.models.user import User


ROLE_PERMISSIONS = {
    UserRole.ADMIN: set(Permission),
    UserRole.SUPERVISOR: {
        Permission.CODEBOOK_MANAGE,
        Permission.RECORD_ASSIGN,
        Permission.REVIEW_APPROVE,
        Permission.EXPORT_GENERATE,
        Permission.DATASET_CREATE,
    },
    UserRole.RESEARCH_LEAD: {
        Permission.CODEBOOK_MANAGE,
        Permission.DATASET_CREATE,
        Permission.EXPORT_GENERATE,
    },
    UserRole.ANNOTATOR: set(),
}


def require_permission(*permissions: Permission):
    def checker(user: User = Depends(get_current_user)) -> User:
        allowed = ROLE_PERMISSIONS.get(user.role, set())
        if not allowed.intersection(permissions):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Insufficient permissions",
            )

        return user

    return checker


def require_role(*roles):
    def checker(user: User = Depends(get_current_user)) -> User:
        if user.role not in roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Insufficient permissions",
            )

        return user

    return checker


ADMIN_ONLY = require_role(
    UserRole.ADMIN,
)

ANNOTATOR_ONLY = require_role(
    UserRole.ANNOTATOR,
)

SUPERVISOR_ONLY = require_role(
    UserRole.SUPERVISOR,
)

ADMIN_OR_SUPERVISOR = require_role(
    UserRole.ADMIN,
    UserRole.SUPERVISOR,
)