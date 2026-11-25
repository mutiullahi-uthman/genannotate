from fastapi import Depends
from fastapi import HTTPException
from fastapi import status

from fastapi.security import HTTPAuthorizationCredentials
from fastapi.security import HTTPBearer

from sqlalchemy.orm import Session

from app.core.enums import UserStatus
from app.core.firebase import firebase_auth
from app.core.logging import logger
from app.database.session import get_db
from app.models.user import User


security = HTTPBearer()


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(
        security,
    ),
    db: Session = Depends(get_db),
) -> User:
    decoded = verify_firebase_token(
        credentials.credentials
    )
    user = (
        db.query(User)
        .filter(
            User.firebase_uid == decoded["uid"]
        )
        .first()
    )

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
        )

    if not user.active or user.status != UserStatus.ACTIVE:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User account is inactive",
        )

    return user


def verify_firebase_token(token: str) -> dict:
    try:
        return firebase_auth.verify_id_token(token)
    except Exception as exc:
        logger.warning(
            "Authentication failed",
            extra={"firebase_error": str(exc)},
        )
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
        ) from exc