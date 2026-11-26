from sqlalchemy import Enum, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.enums import CodebookStatus
from app.database.base import BaseModel, ProjectScopedMixin


class Codebook(ProjectScopedMixin, BaseModel):
    __tablename__ = "codebooks"

    name: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    version: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        index=True,
    )

    status: Mapped[CodebookStatus] = mapped_column(
        Enum(CodebookStatus, name="codebook_status"),
        nullable=False,
        default=CodebookStatus.DRAFT,
    )

    published_by_id = mapped_column(
        ForeignKey("users.id"),
        nullable=True,
    )

    labels = relationship(
        "CodebookLabel",
        back_populates="codebook",
        cascade="all, delete-orphan",
    )