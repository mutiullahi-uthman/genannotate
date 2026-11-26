from sqlalchemy import Enum, ForeignKey, String
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.enums import DatasetStatus
from app.database.base import BaseModel, ProjectScopedMixin


class Dataset(ProjectScopedMixin, BaseModel):
    __tablename__ = "datasets"

    name: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    status: Mapped[DatasetStatus] = mapped_column(
        Enum(DatasetStatus, name="dataset_status"),
        default=DatasetStatus.DRAFT,
        nullable=False,
    )

    language_coverage: Mapped[dict] = mapped_column(
        JSONB,
        nullable=False,
        default=list,
    )

    created_by_id = mapped_column(
        ForeignKey("users.id"),
        nullable=False,
    )

    codebook_id = mapped_column(
        ForeignKey("codebooks.id"),
        nullable=True,
    )

    records = relationship(
        "Record",
        back_populates="dataset",
        cascade="all, delete-orphan",
    )
    versions = relationship(
        "DatasetVersion",
        back_populates="dataset",
        cascade="all, delete-orphan",
        order_by="DatasetVersion.version_number",
    )

    @property
    def latest_version(self):
        return self.versions[-1] if self.versions else None