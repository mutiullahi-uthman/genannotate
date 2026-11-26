from uuid import UUID

from sqlalchemy.orm import Session

from app.models.dataset import Dataset


class DatasetRepository:
    def __init__(
        self,
        db: Session,
    ):
        self.db = db

    def create(
        self,
        dataset: Dataset,
    ) -> Dataset:
        self.db.add(dataset)
        self.db.commit()
        self.db.refresh(dataset)

        return dataset

    def get_by_id(
        self,
        dataset_id: UUID,
    ) -> Dataset | None:
        return (
            self.db.query(Dataset)
            .filter(
                Dataset.id == dataset_id
            )
            .first()
        )

    def get_by_name(
        self,
        name: str,
    ) -> Dataset | None:
        return (
            self.db.query(Dataset)
            .filter(
                Dataset.name == name,
            )
            .first()
        )

    def list_all(
        self,
    ) -> list[Dataset]:
        return (
            self.db.query(Dataset)
            .order_by(
                Dataset.created_at.desc()
            )
            .all()
        )

    def update(
        self,
        dataset: Dataset,
    ) -> Dataset:
        self.db.commit()
        self.db.refresh(dataset)

        return dataset

    def delete(
        self,
        dataset: Dataset,
    ) -> None:
        self.db.delete(dataset)
        self.db.commit()