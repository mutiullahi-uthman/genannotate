from sqlalchemy import Enum
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String

from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from app.core.enums import ImportJobStatus
from app.database.base import BaseModel, ProjectScopedMixin


class ImportJob(ProjectScopedMixin, BaseModel):
    __tablename__ = "import_jobs"

    dataset_id = mapped_column(
        ForeignKey("datasets.id"),
        nullable=False,
    )

    dataset_file_id = mapped_column(
        ForeignKey("dataset_files.id"),
        nullable=False,
    )
    dataset_version_id = mapped_column(
        ForeignKey("dataset_versions.id"),
        nullable=True,
        index=True,
    )

    status: Mapped[ImportJobStatus] = mapped_column(
        Enum(
            ImportJobStatus,
            name="import_job_status",
        ),
        nullable=False,
        default=ImportJobStatus.PENDING,
    )

    total_rows: Mapped[int] = mapped_column(
        Integer,
        default=0,
    )

    valid_rows: Mapped[int] = mapped_column(
        Integer,
        default=0,
    )

    invalid_rows: Mapped[int] = mapped_column(
        Integer,
        default=0,
    )

    error_message: Mapped[str | None] = mapped_column(
        String(2000),
        nullable=True,
    )