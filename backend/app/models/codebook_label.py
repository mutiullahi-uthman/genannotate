from sqlalchemy import ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import BaseModel, ProjectScopedMixin


class CodebookLabel(ProjectScopedMixin, BaseModel):
    __tablename__ = "codebook_labels"

    codebook_id = mapped_column(
        ForeignKey("codebooks.id", ondelete="CASCADE"),
        nullable=False,
    )

    label_name: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
        index=True,
    )

    definition: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    inclusion_guidance: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    exclusion_guidance: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    examples: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    codebook = relationship(
        "Codebook",
        back_populates="labels",
    )