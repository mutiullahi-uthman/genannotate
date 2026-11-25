from app.core.enums import UserRole
from app.core.enums import UserStatus
from app.models.user import User
from app.repositories.user_repository import (
    UserRepository,
)


class UserService:
    def __init__(
        self,
        repository: UserRepository,
    ):
        self.repository = repository

    def get_user_by_firebase_uid(
        self,
        firebase_uid: str,
    ):
        return self.repository.get_by_firebase_uid(
            firebase_uid
        )

    def sync_user(
        self,
        firebase_uid: str,
        email: str,
        full_name: str,
    ):
        existing_user = (
            self.repository.get_by_firebase_uid(
                firebase_uid
            )
        )

        if existing_user:
            changed = False

            if existing_user.email != email:
                existing_user.email = email
                changed = True

            if (
                existing_user.full_name
                != full_name
            ):
                existing_user.full_name = full_name
                changed = True

            if changed:
                return self.repository.update(
                    existing_user
                )

            return existing_user

        user = User(
            firebase_uid=firebase_uid,
            email=email,
            full_name=full_name,
            role=UserRole.ANNOTATOR,
            status=UserStatus.ACTIVE,
            active=True,
        )

        return self.repository.create(
            user
        )