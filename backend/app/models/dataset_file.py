from sqlalchemy import BigInteger, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column

from app.database.base import BaseModel


class DatasetFile(BaseModel):
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

    blob_path: Mapped[str] = mapped_column(
        String(1000),
        nullable=False,
    )

    cdn_url: Mapped[str] = mapped_column(
        String(1000),
        nullable=False,
    )

    checksum: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    uploaded_by_id = mapped_column(
        ForeignKey("users.id"),
        nullable=False,
    )