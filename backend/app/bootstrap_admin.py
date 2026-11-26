import argparse
import sys
from collections.abc import Sequence

from sqlalchemy import func, select, text
from sqlalchemy.orm import Session

from app.core.enums import UserRole, UserStatus
from app.database.session import SessionLocal
from app.models.project import Project, ProjectMembership
from app.models.user import User


class BootstrapAdminError(RuntimeError):
    pass


def bootstrap_first_admin(db: Session, email: str) -> str:
    normalized_email = email.strip().lower()
    if not normalized_email:
        raise BootstrapAdminError("An email address is required.")

    with db.begin():
        db.execute(
            text("SELECT pg_advisory_xact_lock(:lock_id)"),
            {"lock_id": 0x47454E414E4E},
        )

        default_project_id = db.scalar(
            select(Project.id).where(Project.slug == "default")
        )
        if default_project_id is None:
            raise BootstrapAdminError(
                "The default project is missing. Apply database migrations first."
            )

        existing_admin_id = db.scalar(
            select(ProjectMembership.id)
            .where(
                ProjectMembership.project_id == default_project_id,
                ProjectMembership.role == UserRole.ADMIN,
                ProjectMembership.active.is_(True),
            )
            .limit(1)
        )
        if existing_admin_id is not None:
            raise BootstrapAdminError(
                "An Admin already exists. Use the application to manage roles."
            )

        matching_users = db.scalars(
            select(User)
            .where(func.lower(User.email) == normalized_email)
            .limit(2)
        ).all()
        if not matching_users:
            raise BootstrapAdminError(
                "No account matches that email. Sign in once first, then retry."
            )
        if len(matching_users) > 1:
            raise BootstrapAdminError(
                "Multiple accounts match that email; resolve the duplicate before retrying."
            )

        user = matching_users[0]
        if not user.active or user.status != UserStatus.ACTIVE:
            raise BootstrapAdminError(
                "The matching account is not active and cannot be promoted."
            )

        membership = db.scalar(
            select(ProjectMembership).where(
                ProjectMembership.project_id == default_project_id,
                ProjectMembership.user_id == user.id,
            )
        )
        if membership is None:
            raise BootstrapAdminError(
                "The account is not a member of the default project."
            )
        if not membership.active:
            raise BootstrapAdminError(
                "The account's default-project membership is inactive."
            )

        promoted_email = user.email
        membership.role = UserRole.ADMIN

    return promoted_email


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Promote one existing account to the first GenAnnotate Admin."
    )
    parser.add_argument(
        "--email",
        required=True,
        help="Email of the account that has already signed in to GenAnnotate",
    )
    args = parser.parse_args(argv)

    try:
        with SessionLocal() as db:
            promoted_email = bootstrap_first_admin(db, args.email)
    except BootstrapAdminError as exc:
        print(f"Admin bootstrap failed: {exc}", file=sys.stderr)
        return 1

    print(f"First Admin access granted to {promoted_email}.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
