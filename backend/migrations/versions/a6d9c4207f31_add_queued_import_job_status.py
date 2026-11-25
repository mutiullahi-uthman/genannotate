"""add queued import job status

Revision ID: a6d9c4207f31
Revises: 1edd975d03e9
Create Date: 2026-11-24 16:00:00

"""
from typing import Sequence, Union

from alembic import op


revision: str = "a6d9c4207f31"
down_revision: Union[str, Sequence[str], None] = "1edd975d03e9"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute(
        "ALTER TYPE import_job_status ADD VALUE IF NOT EXISTS 'QUEUED'"
    )


def downgrade() -> None:
    op.execute(
        "UPDATE import_jobs SET status = 'PENDING' WHERE status = 'QUEUED'"
    )
    op.execute(
        "ALTER TYPE import_job_status RENAME TO import_job_status_old"
    )
    op.execute(
        "CREATE TYPE import_job_status AS ENUM "
        "('PENDING', 'VALIDATING', 'VALIDATION_FAILED', 'VALIDATED', "
        "'IMPORTING', 'COMPLETED', 'FAILED')"
    )
    op.execute(
        "ALTER TABLE import_jobs ALTER COLUMN status TYPE import_job_status "
        "USING status::text::import_job_status"
    )
    op.execute("DROP TYPE import_job_status_old")
