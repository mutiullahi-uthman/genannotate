from sqlalchemy import Boolean, Enum, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.enums import (
    AnnotationStatus,
    CulturalFlag,
    FrequencyCategory,
    RiskLevel,
)
from app.database.base import BaseModel, ProjectScopedMixin


class Annotation(ProjectScopedMixin, BaseModel):
    __tablename__ = "annotations"

    record_id = mapped_column(
        ForeignKey("records.id"),
        nullable=False,
        index=True,
    )

    annotator_id = mapped_column(
        ForeignKey("users.id"),
        nullable=False,
    )

    version_number: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=1,
    )

    parent_annotation_id = mapped_column(
        ForeignKey("annotations.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )

    construct: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    evidence_span: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    frequency: Mapped[FrequencyCategory] = mapped_column(
        Enum(
            FrequencyCategory,
            name="frequency_category",
        ),
        nullable=False,
    )

    cultural_flag: Mapped[CulturalFlag] = mapped_column(
        Enum(
            CulturalFlag,
            name="cultural_flag",
        ),
        nullable=False,
        default=CulturalFlag.NONE,
    )

    cultural_note: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    risk_level: Mapped[RiskLevel] = mapped_column(
        Enum(
            RiskLevel,
            name="risk_level",
        ),
        nullable=False,
    )

    risk_rationale: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    status: Mapped[AnnotationStatus] = mapped_column(
        Enum(
            AnnotationStatus,
            name="annotation_status",
        ),
        nullable=False,
        default=AnnotationStatus.DRAFT,
    )

    is_latest: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False,
    )

    record = relationship("Record")