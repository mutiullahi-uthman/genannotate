from app.core.enums import UserRole, UserStatus
from app.models.user import User
from app.models.project import Project, ProjectMembership
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

        default_project = (
            self.repository.db.query(Project)
            .filter(Project.slug == "default")
            .first()
        )
        if default_project is None:
            raise RuntimeError(
                "The default project is missing; apply database migrations first."
            )

        user = User(
            firebase_uid=firebase_uid,
            email=email,
            full_name=full_name,
            status=UserStatus.ACTIVE,
            active=True,
        )

        self.repository.db.add(user)
        self.repository.db.flush()
        self.repository.db.add(
            ProjectMembership(
                project_id=default_project.id,
                user_id=user.id,
                role=UserRole.ANNOTATOR,
                active=True,
            )
        )
        self.repository.db.commit()
        self.repository.db.refresh(user)
        return user