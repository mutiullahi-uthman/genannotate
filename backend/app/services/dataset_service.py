from fastapi import HTTPException, status

from app.core.enums import DatasetStatus
from app.models.dataset import Dataset
from app.repositories.dataset_repository import DatasetRepository


class DatasetService:
    def __init__(self, repository: DatasetRepository):
        self.repository = repository

    def create_dataset(
        self,
        name,
        version,
        language_coverage,
        created_by_id,
    ):
        existing = self.repository.get_by_name_and_version(name, version)
        if existing:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Dataset version already exists",
            )

        dataset = Dataset(
            name=name,
            version=version,
            language_coverage=language_coverage,
            status=DatasetStatus.ACTIVE,
            created_by_id=created_by_id,
        )

        return self.repository.create(dataset)

    def list_datasets(self):
        return self.repository.list_all()

    def get_dataset(self, dataset_id):
        dataset = self.repository.get_by_id(dataset_id)
        if not dataset:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Dataset not found",
            )

        return dataset

    def update_dataset(self, dataset_id, payload):
        dataset = self.get_dataset(dataset_id)

        if payload.name is not None:
            dataset.name = payload.name
        if payload.status is not None:
            dataset.status = payload.status
        if payload.language_coverage is not None:
            dataset.language_coverage = payload.language_coverage

        return self.repository.update(dataset)

    def delete_dataset(self, dataset_id):
        dataset = self.get_dataset(dataset_id)
        self.repository.delete(dataset)
