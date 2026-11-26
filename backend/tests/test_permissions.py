import unittest
from types import SimpleNamespace

from fastapi import HTTPException

from app.core.enums import Permission, UserRole
from app.core.permissions import require_permission


class PermissionTests(unittest.TestCase):
    def test_permission_check_returns_the_project_membership(self):
        membership = SimpleNamespace(role=UserRole.SUPERVISOR)

        result = require_permission(Permission.RECORD_ASSIGN)(membership)

        self.assertIs(result, membership)

    def test_permission_check_rejects_roles_without_access(self):
        membership = SimpleNamespace(role=UserRole.ANNOTATOR)

        with self.assertRaises(HTTPException) as raised:
            require_permission(Permission.RECORD_ASSIGN)(membership)

        self.assertEqual(raised.exception.status_code, 403)


if __name__ == "__main__":
    unittest.main()
