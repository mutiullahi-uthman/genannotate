from sqlalchemy import Enum, ForeignKey, Integer, String
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column

from app.core.enums import ExportFormat, ExportStatus
from app.database.base import BaseModel


class Export(BaseModel):
    __tablename__ = "exports"

    dataset_id: Mapped[str] = mapped_column(
        ForeignKey("datasets.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    requested_by_id: Mapped[str] = mapped_column(
        ForeignKey("users.id"),
        nullable=False,
        index=True,
    )

    export_identifier: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
        unique=True,
        index=True,
    )

    export_format: Mapped[ExportFormat] = mapped_column(
        Enum(
            ExportFormat,
            name="export_format",
        ),
        nullable=False,
    )

    status: Mapped[ExportStatus] = mapped_column(
        Enum(
            ExportStatus,
            name="export_status",
        ),
        nullable=False,
        default=ExportStatus.PENDING,
    )

    file_path: Mapped[str | None] = mapped_column(
        String(1000),
        nullable=True,
    )

    cdn_url: Mapped[str | None] = mapped_column(
        String(1000),
        nullable=True,
    )

    filters: Mapped[dict] = mapped_column(
        JSONB,
        nullable=False,
        default=dict,
    )

    record_count: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=0,
    )

    exported_at: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
    )