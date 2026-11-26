from sqlalchemy import BigInteger, Boolean, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column

from app.database.base import BaseModel, ProjectScopedMixin


class DatasetFile(ProjectScopedMixin, BaseModel):
    __tablename__ = "dataset_files"

    dataset_id = mapped_column(
        ForeignKey("datasets.id"),
        nullable=False,
    )

    file_name: Mapped[str] = mapped_column(
        String(500),
        nullable=False,
    )

    mime_type: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    file_size: Mapped[int] = mapped_column(
        BigInteger,
        nullable=False,
    )

    object_key: Mapped[str] = mapped_column(
        String(1000),
        nullable=False,
    )

    checksum: Mapped[str] = mapped_column(
        String(255),
        nullable=True,
    )

    upload_complete: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=False,
    )

    dataset_version_id = mapped_column(
        ForeignKey("dataset_versions.id"),
        nullable=True,
        index=True,
    )

    uploaded_by_id = mapped_column(
        ForeignKey("users.id"),
        nullable=False,
    )