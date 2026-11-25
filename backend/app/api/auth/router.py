from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from fastapi import Request
from fastapi import status
from fastapi.security import HTTPAuthorizationCredentials
from fastapi.security import HTTPBearer
from sqlalchemy.orm import Session

from app.core.auth import get_current_user
from app.core.auth import verify_firebase_token
from app.core.rate_limit import limiter
from app.database.session import get_db

from app.models.user import User

from app.schemas.user import MeResponse

from app.repositories.user_repository import (
    UserRepository,
)

from app.services.user_service import (
    UserService,
)

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)
security = HTTPBearer()

# GET /auth/me - Get the current authenticated user
@router.get(
    "/me",
    response_model=MeResponse,
)
def get_me(
    current_user: User = Depends(
        get_current_user
    ),
):
    return current_user

# POST /auth/sync-user - Create or refresh the local Firebase user profile
@router.post(
    "/sync-user",
    response_model=MeResponse,
)
@limiter.limit("100/minute")
def sync_user(
    request: Request,
    db: Session = Depends(get_db),
    credentials: HTTPAuthorizationCredentials = Depends(
        security
    ),
):
    identity = verify_firebase_token(
        credentials.credentials
    )
    email = identity.get("email")
    if not email:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Firebase account must include an email address",
        )

    repository = UserRepository(db)

    service = UserService(
        repository
    )

    return service.sync_user(
        firebase_uid=identity["uid"],
        email=email,
        full_name=identity.get("name") or email,
    )

