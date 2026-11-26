from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.core.auth import get_current_user
from app.core.enums import RecordState, UserRole
from app.core.project_context import get_active_project_membership
from app.database.session import get_db
from app.models.project import ProjectMembership
from app.models.record import Record
from app.models.user import User


router = APIRouter(prefix="/records", tags=["Records"])


class RecordWorkspaceResponse(BaseModel):
    id: UUID
    dataset_id: UUID
    dataset_version_id: UUID
    record_id: str
    language: str
    instrument: str
    item_id: str
    item_text: str | None
    transcript: str
    audio_link: str | None
    state: RecordState

    model_config = {"from_attributes": True}


@router.get("/{record_id}", response_model=RecordWorkspaceResponse)
def get_record(
    record_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    membership: ProjectMembership = Depends(
        get_active_project_membership
    ),
):
    record = (
        db.query(Record)
        .filter(Record.id == record_id)
        .first()
    )
    if record is None or (
        membership.role == UserRole.ANNOTATOR
        and record.assignee_id != current_user.id
    ):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Record not found",
        )
    return record
