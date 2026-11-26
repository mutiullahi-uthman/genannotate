from datetime import datetime

from sqlalchemy import DateTime, Enum, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.enums import RecordState
from app.database.base import BaseModel, ProjectScopedMixin


class Record(ProjectScopedMixin, BaseModel):
    __tablename__ = "records"

    dataset_id = mapped_column(
        ForeignKey("datasets.id"),
        nullable=False,
        index=True,
    )
    dataset_version_id = mapped_column(
        ForeignKey("dataset_versions.id"),
        nullable=False,
        index=True,
    )

    record_id: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
        index=True,
    )

    language: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    instrument: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    item_id: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    item_text: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    transcript: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    audio_link: Mapped[str | None] = mapped_column(
        String(1000),
        nullable=True,
    )

    state: Mapped[RecordState] = mapped_column(
        Enum(RecordState, name="record_state"),
        default=RecordState.IMPORTED,
        nullable=False,
    )

    assignee_id = mapped_column(
        ForeignKey("users.id"),
        nullable=True,
    )

    locked_by_id = mapped_column(
        ForeignKey("users.id"),
        nullable=True,
    )

    locked_until: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )

    dataset = relationship(
        "Dataset",
        back_populates="records",
    )