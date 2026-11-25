from sqlalchemy import Enum
from sqlalchemy import ForeignKey

from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from app.core.enums import AssignmentType
from app.database.base import BaseModel


class Assignment(BaseModel):
    __tablename__ = "assignments"

    record_id = mapped_column(
        ForeignKey(
            "records.id",
            ondelete="CASCADE",
        ),
        nullable=False,
        index=True,
    )

    old_assignee_id = mapped_column(
        ForeignKey("users.id"),
        nullable=True,
    )

    new_assignee_id = mapped_column(
        ForeignKey("users.id"),
        nullable=False,
        index=True,
    )

    assigned_by_id = mapped_column(
        ForeignKey("users.id"),
        nullable=False,
    )

    assignment_type: Mapped[
        AssignmentType
    ] = mapped_column(
        Enum(
            AssignmentType,
            name="assignment_type",
        ),
        nullable=False,
    )