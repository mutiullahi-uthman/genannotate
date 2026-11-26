import unittest
from contextlib import nullcontext
from types import SimpleNamespace
from unittest.mock import Mock
from uuid import uuid4

from app.bootstrap_admin import (
    BootstrapAdminError,
    bootstrap_first_admin,
)
from app.core.enums import UserRole, UserStatus


class BootstrapAdminTests(unittest.TestCase):
    def setUp(self):
        self.db = Mock()
        self.db.begin.return_value = nullcontext()

    def test_promotes_an_existing_active_user_when_no_admin_exists(self):
        user = SimpleNamespace(
            id=uuid4(),
            email="admin@example.com",
            status=UserStatus.ACTIVE,
            active=True,
        )
        project_id = uuid4()
        membership = SimpleNamespace(
            active=True,
            role=UserRole.ANNOTATOR,
        )
        self.db.scalar.side_effect = [project_id, None, membership]
        self.db.scalars.return_value.all.return_value = [user]

        promoted_email = bootstrap_first_admin(self.db, " ADMIN@example.com ")

        self.assertEqual(promoted_email, "admin@example.com")
        self.assertEqual(membership.role, UserRole.ADMIN)
        self.db.execute.assert_called_once()

    def test_refuses_to_promote_when_an_admin_already_exists(self):
        self.db.scalar.return_value = "existing-admin-id"

        with self.assertRaisesRegex(BootstrapAdminError, "already exists"):
            bootstrap_first_admin(self.db, "admin@example.com")

        self.db.scalars.assert_not_called()

    def test_requires_account_to_sign_in_before_bootstrap(self):
        self.db.scalar.side_effect = [uuid4(), None]
        self.db.scalars.return_value.all.return_value = []

        with self.assertRaisesRegex(BootstrapAdminError, "Sign in once first"):
            bootstrap_first_admin(self.db, "admin@example.com")

    def test_refuses_inactive_accounts(self):
        user = SimpleNamespace(
            email="admin@example.com",
            status=UserStatus.SUSPENDED,
            active=False,
        )
        self.db.scalar.side_effect = [uuid4(), None]
        self.db.scalars.return_value.all.return_value = [user]

        with self.assertRaisesRegex(BootstrapAdminError, "not active"):
            bootstrap_first_admin(self.db, "admin@example.com")

        self.assertEqual(user.status, UserStatus.SUSPENDED)


if __name__ == "__main__":
    unittest.main()
