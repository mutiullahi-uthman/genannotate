from sqlalchemy import Enum, ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.core.enums import (
    ReviewDecision,
    ReviewStatus,
)
from app.database.base import BaseModel, ProjectScopedMixin


class Review(ProjectScopedMixin, BaseModel):
    __tablename__ = "reviews"

    record_id = mapped_column(
        ForeignKey("records.id"),
        nullable=False,
        index=True,
    )

    reviewer_id = mapped_column(
        ForeignKey("users.id"),
        nullable=False,
    )

    decision: Mapped[ReviewDecision] = mapped_column(
        Enum(
            ReviewDecision,
            name="review_decision",
        ),
        nullable=False,
    )

    status: Mapped[ReviewStatus] = mapped_column(
        Enum(
            ReviewStatus,
            name="review_status",
        ),
        nullable=False,
    )

    comments: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    reason_for_change: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )