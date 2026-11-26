from uuid import UUID

from fastapi import APIRouter
from fastapi import Depends
from fastapi import Response
from fastapi import status

from sqlalchemy.orm import Session

from app.core.auth import get_current_user
from app.core.enums import Permission
from app.core.permissions import require_permission
from app.database.session import get_db

from app.repositories.dataset_repository import (
    DatasetRepository,
)

from app.schemas.dataset import (
    DatasetCreate,
    DatasetResponse,
    DatasetUpdate,
)

from app.services.dataset_service import (
    DatasetService,
)


router = APIRouter(
    prefix="/datasets",
    tags=["Datasets"],
)

# Create a new dataset

@router.post(
    "",
    response_model=DatasetResponse,
    dependencies=[Depends(require_permission(Permission.DATASET_CREATE))],
)
def create_dataset(
    payload: DatasetCreate,
    db: Session = Depends(get_db),
    current_user=Depends(
        get_current_user,
    ),
):
    repository = DatasetRepository(db)

    service = DatasetService(
        repository
    )

    return service.create_dataset(
        name=payload.name,
        language_coverage=payload.language_coverage,
        created_by_id=current_user.id,
    )

# List all datasets
@router.get(
    "",
    response_model=list[DatasetResponse],
)
def list_datasets(
    db: Session = Depends(get_db),
):
    repository = DatasetRepository(db)

    service = DatasetService(
        repository
    )

    return service.list_datasets()

# GET a dataset by ID
@router.get(
    "/{dataset_id}",
    response_model=DatasetResponse,
)
def get_dataset(
    dataset_id: UUID,
    db: Session = Depends(get_db),
):
    service = DatasetService(
        DatasetRepository(db)
    )

    return service.get_dataset(
        dataset_id
    )
    
# PATCH a dataset by ID
@router.patch(
    "/{dataset_id}",
    response_model=DatasetResponse,
    dependencies=[Depends(require_permission(Permission.DATASET_CREATE))],
)
def update_dataset(
    dataset_id: UUID,
    payload: DatasetUpdate,
    db: Session = Depends(get_db),
):
    service = DatasetService(
        DatasetRepository(db)
    )

    return service.update_dataset(
        dataset_id,
        payload,
    )
    
# DELETE a dataset by ID
@router.delete(
    "/{dataset_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(require_permission(Permission.DATASET_DELETE))],
)
def delete_dataset(
    dataset_id: UUID,
    db: Session = Depends(get_db),
):
    service = DatasetService(
        DatasetRepository(db)
    )

    service.delete_dataset(
        dataset_id
    )

    return Response(
        status_code=status.HTTP_204_NO_CONTENT
    )        