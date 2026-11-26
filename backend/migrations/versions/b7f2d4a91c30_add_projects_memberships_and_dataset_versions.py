"""Add project-scoped roles and immutable dataset versions.

Revision ID: b7f2d4a91c30
Revises: a6d9c4207f31
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


revision: str = "b7f2d4a91c30"
down_revision: Union[str, Sequence[str], None] = "a6d9c4207f31"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

DEFAULT_PROJECT_ID = "00000000-0000-0000-0000-000000000001"


def _add_project_column(table_name: str) -> None:
    op.add_column(
        table_name,
        sa.Column("project_id", sa.UUID(), nullable=True),
    )
    op.execute(
        sa.text(
            f"UPDATE {table_name} "
            "SET project_id = CAST(:project_id AS uuid)"
        ).bindparams(project_id=DEFAULT_PROJECT_ID)
    )
    op.alter_column(table_name, "project_id", nullable=False)
    op.create_foreign_key(
        f"fk_{table_name}_project_id_projects",
        table_name,
        "projects",
        ["project_id"],
        ["id"],
        ondelete="CASCADE",
    )
    op.create_index(
        f"ix_{table_name}_project_id",
        table_name,
        ["project_id"],
        unique=False,
    )


def upgrade() -> None:
    op.create_table(
        "projects",
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("slug", sa.String(length=100), nullable=False),
        sa.Column("active", sa.Boolean(), nullable=False, server_default=sa.true()),
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_projects")),
        sa.UniqueConstraint("slug", name=op.f("uq_projects_slug")),
    )
    op.execute(
        sa.text(
            "INSERT INTO projects (id, name, slug, active) "
            "VALUES (CAST(:id AS uuid), 'GenAnnotate', 'default', true)"
        ).bindparams(id=DEFAULT_PROJECT_ID)
    )

    op.create_table(
        "project_memberships",
        sa.Column("project_id", sa.UUID(), nullable=False),
        sa.Column("user_id", sa.UUID(), nullable=False),
        sa.Column(
            "role",
            postgresql.ENUM(
                "ADMIN",
                "ANNOTATOR",
                "SUPERVISOR",
                "RESEARCH_LEAD",
                name="user_role",
                create_type=False,
            ),
            nullable=False,
        ),
        sa.Column("active", sa.Boolean(), nullable=False, server_default=sa.true()),
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(
            ["project_id"],
            ["projects.id"],
            name=op.f("fk_project_memberships_project_id_projects"),
            ondelete="CASCADE",
        ),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["users.id"],
            name=op.f("fk_project_memberships_user_id_users"),
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_project_memberships")),
        sa.UniqueConstraint(
            "project_id",
            "user_id",
            name="uq_project_memberships_project_user",
        ),
    )
    op.create_index(
        "ix_project_memberships_project_id",
        "project_memberships",
        ["project_id"],
    )
    op.create_index(
        "ix_project_memberships_user_id",
        "project_memberships",
        ["user_id"],
    )
    op.execute(
        sa.text(
            "INSERT INTO project_memberships "
            "(id, project_id, user_id, role, active) "
            "SELECT gen_random_uuid(), CAST(:project_id AS uuid), "
            "id, role, active FROM users"
        ).bindparams(project_id=DEFAULT_PROJECT_ID)
    )

    _add_project_column("datasets")
    op.create_table(
        "dataset_versions",
        sa.Column("project_id", sa.UUID(), nullable=False),
        sa.Column("dataset_id", sa.UUID(), nullable=False),
        sa.Column("version_number", sa.Integer(), nullable=False),
        sa.Column("label", sa.String(length=100), nullable=False),
        sa.Column("imported_by_id", sa.UUID(), nullable=True),
        sa.Column(
            "imported_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(
            ["dataset_id"],
            ["datasets.id"],
            name=op.f("fk_dataset_versions_dataset_id_datasets"),
            ondelete="CASCADE",
        ),
        sa.ForeignKeyConstraint(
            ["imported_by_id"],
            ["users.id"],
            name=op.f("fk_dataset_versions_imported_by_id_users"),
        ),
        sa.ForeignKeyConstraint(
            ["project_id"],
            ["projects.id"],
            name=op.f("fk_dataset_versions_project_id_projects"),
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_dataset_versions")),
        sa.UniqueConstraint(
            "dataset_id",
            "version_number",
            name="uq_dataset_versions_dataset_number",
        ),
    )
    op.create_index(
        "ix_dataset_versions_project_id",
        "dataset_versions",
        ["project_id"],
    )
    op.create_index(
        "ix_dataset_versions_dataset_id",
        "dataset_versions",
        ["dataset_id"],
    )
    op.execute(
        sa.text(
            "INSERT INTO dataset_versions "
            "(id, project_id, dataset_id, version_number, label, imported_by_id, imported_at) "
            "SELECT gen_random_uuid(), project_id, id, 1, version, created_by_id, created_at "
            "FROM datasets"
        )
    )

    for table_name in (
        "dataset_files",
        "import_jobs",
        "records",
        "annotations",
        "reviews",
        "assignments",
        "audit_events",
        "codebooks",
        "codebook_labels",
        "exports",
        "dashboard_metrics",
    ):
        _add_project_column(table_name)

    op.add_column(
        "records",
        sa.Column("dataset_version_id", sa.UUID(), nullable=True),
    )
    op.execute(
        sa.text(
            "UPDATE records r SET dataset_version_id = v.id "
            "FROM dataset_versions v WHERE v.dataset_id = r.dataset_id"
        )
    )
    op.alter_column("records", "dataset_version_id", nullable=False)
    op.create_foreign_key(
        "fk_records_dataset_version_id_dataset_versions",
        "records",
        "dataset_versions",
        ["dataset_version_id"],
        ["id"],
    )
    op.create_index(
        "ix_records_dataset_version_id",
        "records",
        ["dataset_version_id"],
    )

    op.add_column(
        "dataset_files",
        sa.Column("dataset_version_id", sa.UUID(), nullable=True),
    )
    op.execute(
        sa.text(
            "UPDATE dataset_files f SET dataset_version_id = v.id "
            "FROM dataset_versions v WHERE v.dataset_id = f.dataset_id"
        )
    )
    op.create_foreign_key(
        "fk_dataset_files_dataset_version_id_dataset_versions",
        "dataset_files",
        "dataset_versions",
        ["dataset_version_id"],
        ["id"],
    )
    op.create_index(
        "ix_dataset_files_dataset_version_id",
        "dataset_files",
        ["dataset_version_id"],
    )
    op.add_column(
        "dataset_files",
        sa.Column(
            "upload_complete",
            sa.Boolean(),
            nullable=False,
            server_default=sa.true(),
        ),
    )
    op.alter_column("dataset_files", "upload_complete", server_default=None)
    op.alter_column("dataset_files", "blob_path", new_column_name="object_key")
    op.drop_column("dataset_files", "cdn_url")

    op.add_column(
        "import_jobs",
        sa.Column("dataset_version_id", sa.UUID(), nullable=True),
    )
    op.create_foreign_key(
        "fk_import_jobs_dataset_version_id_dataset_versions",
        "import_jobs",
        "dataset_versions",
        ["dataset_version_id"],
        ["id"],
    )
    op.create_index(
        "ix_import_jobs_dataset_version_id",
        "import_jobs",
        ["dataset_version_id"],
    )

    op.alter_column("exports", "file_path", new_column_name="object_key")
    op.drop_column("exports", "cdn_url")

    op.drop_index("ix_dashboard_metrics_metric_date", table_name="dashboard_metrics")
    op.create_unique_constraint(
        "uq_dashboard_metrics_project_date",
        "dashboard_metrics",
        ["project_id", "metric_date"],
    )

    op.drop_column("datasets", "version")
    op.drop_column("users", "role")


def downgrade() -> None:
    op.add_column(
        "users",
        sa.Column(
            "role",
            postgresql.ENUM(
                "ADMIN",
                "ANNOTATOR",
                "SUPERVISOR",
                "RESEARCH_LEAD",
                name="user_role",
                create_type=False,
            ),
            nullable=True,
        ),
    )
    op.execute(
        sa.text(
            "UPDATE users u SET role = m.role FROM project_memberships m "
            "JOIN projects p ON p.id = m.project_id "
            "WHERE m.user_id = u.id AND p.slug = 'default'"
        )
    )
    op.alter_column("users", "role", nullable=False)
    op.add_column(
        "datasets",
        sa.Column("version", sa.String(length=100), nullable=True),
    )
    op.execute(
        sa.text(
            "UPDATE datasets d SET version = v.label FROM dataset_versions v "
            "WHERE v.dataset_id = d.id AND v.version_number = "
            "(SELECT max(v2.version_number) FROM dataset_versions v2 "
            "WHERE v2.dataset_id = d.id)"
        )
    )
    op.alter_column("datasets", "version", nullable=False)

    op.drop_constraint(
        "uq_dashboard_metrics_project_date",
        "dashboard_metrics",
        type_="unique",
    )
    op.create_index(
        "ix_dashboard_metrics_metric_date",
        "dashboard_metrics",
        ["metric_date"],
        unique=True,
    )
    op.alter_column("exports", "object_key", new_column_name="file_path")
    op.add_column(
        "exports",
        sa.Column("cdn_url", sa.String(length=1000), nullable=True),
    )
    op.drop_index("ix_import_jobs_dataset_version_id", table_name="import_jobs")
    op.drop_constraint(
        "fk_import_jobs_dataset_version_id_dataset_versions",
        "import_jobs",
        type_="foreignkey",
    )
    op.drop_column("import_jobs", "dataset_version_id")
    op.add_column(
        "dataset_files",
        sa.Column("cdn_url", sa.String(length=1000), nullable=True),
    )
    op.alter_column("dataset_files", "object_key", new_column_name="blob_path")
    op.drop_column("dataset_files", "upload_complete")
    op.drop_index(
        "ix_dataset_files_dataset_version_id",
        table_name="dataset_files",
    )
    op.drop_constraint(
        "fk_dataset_files_dataset_version_id_dataset_versions",
        "dataset_files",
        type_="foreignkey",
    )
    op.drop_column("dataset_files", "dataset_version_id")
    op.drop_index("ix_records_dataset_version_id", table_name="records")
    op.drop_constraint(
        "fk_records_dataset_version_id_dataset_versions",
        "records",
        type_="foreignkey",
    )
    op.drop_column("records", "dataset_version_id")

    for table_name in (
        "dashboard_metrics",
        "exports",
        "codebook_labels",
        "codebooks",
        "audit_events",
        "assignments",
        "reviews",
        "annotations",
        "records",
        "import_jobs",
        "dataset_files",
        "datasets",
    ):
        op.drop_index(f"ix_{table_name}_project_id", table_name=table_name)
        op.drop_constraint(
            f"fk_{table_name}_project_id_projects",
            table_name,
            type_="foreignkey",
        )
        op.drop_column(table_name, "project_id")

    op.drop_index("ix_dataset_versions_dataset_id", table_name="dataset_versions")
    op.drop_index("ix_dataset_versions_project_id", table_name="dataset_versions")
    op.drop_table("dataset_versions")
    op.drop_index("ix_project_memberships_user_id", table_name="project_memberships")
    op.drop_index(
        "ix_project_memberships_project_id",
        table_name="project_memberships",
    )
    op.drop_table("project_memberships")
    op.drop_table("projects")
