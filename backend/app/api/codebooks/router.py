from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session, selectinload

from app.core.auth import get_current_user
from app.core.enums import CodebookStatus, Permission
from app.core.permissions import require_permission
from app.database.session import get_db
from app.models.codebook import Codebook
from app.models.codebook_label import CodebookLabel
from app.models.user import User
from app.schemas.codebook import (
    CodebookCreate,
    CodebookLabelCreate,
    CodebookLabelResponse,
    CodebookLabelUpdate,
    CodebookResponse,
    CodebookUpdate,
)

router = APIRouter(
    prefix="/codebooks",
    tags=["Codebooks"],
)
MANAGE_CODEBOOKS = Depends(
    require_permission(Permission.CODEBOOK_MANAGE)
)


@router.get("", response_model=list[CodebookResponse])
def list_codebooks(
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
):
    return (
        db.query(Codebook)
        .options(selectinload(Codebook.labels))
        .order_by(Codebook.created_at.desc())
        .all()
    )


@router.post(
    "",
    response_model=CodebookResponse,
    status_code=status.HTTP_201_CREATED,
    dependencies=[MANAGE_CODEBOOKS],
)
def create_codebook(
    payload: CodebookCreate,
    db: Session = Depends(get_db),
):
    codebook = Codebook(
        name=payload.name,
        version=payload.version,
        status=CodebookStatus.DRAFT,
    )
    db.add(codebook)
    db.commit()
    db.refresh(codebook)
    return codebook


@router.patch(
    "/{codebook_id}",
    response_model=CodebookResponse,
    dependencies=[MANAGE_CODEBOOKS],
)
def update_codebook(
    codebook_id: UUID,
    payload: CodebookUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    codebook = (
        db.query(Codebook)
        .options(selectinload(Codebook.labels))
        .filter(Codebook.id == codebook_id)
        .first()
    )
    if not codebook:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Codebook not found",
        )

    if (
        payload.status == CodebookStatus.PUBLISHED
        and not codebook.labels
    ):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="A codebook must contain at least one label before publishing",
        )

    if (
        codebook.status != CodebookStatus.DRAFT
        and (payload.name is not None or payload.version is not None)
    ):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Published codebooks cannot be edited; create a new version instead",
        )
    if (
        (
            codebook.status == CodebookStatus.PUBLISHED
            and payload.status == CodebookStatus.DRAFT
        )
        or (
            codebook.status == CodebookStatus.ARCHIVED
            and payload.status not in (None, CodebookStatus.ARCHIVED)
        )
    ):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Codebook status cannot be moved back to an earlier stage",
        )

    if payload.name is not None:
        codebook.name = payload.name
    if payload.version is not None:
        codebook.version = payload.version
    if payload.status is not None:
        codebook.status = payload.status
        if payload.status == CodebookStatus.PUBLISHED:
            codebook.published_by_id = current_user.id

    db.commit()
    db.refresh(codebook)
    return codebook


@router.post(
    "/{codebook_id}/labels",
    response_model=CodebookLabelResponse,
    status_code=status.HTTP_201_CREATED,
    dependencies=[MANAGE_CODEBOOKS],
)
def create_label(
    codebook_id: UUID,
    payload: CodebookLabelCreate,
    db: Session = Depends(get_db),
):
    codebook = db.query(Codebook).filter(
        Codebook.id == codebook_id
    ).first()
    if not codebook:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Codebook not found",
        )
    if codebook.status != CodebookStatus.DRAFT:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Labels can only be changed on draft codebooks",
        )

    label = CodebookLabel(
        codebook_id=codebook_id,
        **payload.model_dump(),
    )
    db.add(label)
    db.commit()
    db.refresh(label)
    return label


@router.patch(
    "/{codebook_id}/labels/{label_id}",
    response_model=CodebookLabelResponse,
    dependencies=[MANAGE_CODEBOOKS],
)
def update_label(
    codebook_id: UUID,
    label_id: UUID,
    payload: CodebookLabelUpdate,
    db: Session = Depends(get_db),
):
    label = (
        db.query(CodebookLabel)
        .join(Codebook)
        .filter(
            Codebook.id == codebook_id,
            CodebookLabel.id == label_id,
        )
        .first()
    )
    if not label:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Codebook label not found",
        )
    if label.codebook.status != CodebookStatus.DRAFT:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Labels can only be changed on draft codebooks",
        )

    for field, value in payload.model_dump(exclude_unset=True).items():
        if value is not None or field not in {"label_name", "definition"}:
            setattr(label, field, value)
    db.commit()
    db.refresh(label)
    return label


@router.delete(
    "/{codebook_id}/labels/{label_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[MANAGE_CODEBOOKS],
)
def delete_label(
    codebook_id: UUID,
    label_id: UUID,
    db: Session = Depends(get_db),
):
    label = (
        db.query(CodebookLabel)
        .join(Codebook)
        .filter(
            Codebook.id == codebook_id,
            CodebookLabel.id == label_id,
        )
        .first()
    )
    if not label:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Codebook label not found",
        )
    if label.codebook.status != CodebookStatus.DRAFT:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Labels can only be changed on draft codebooks",
        )

    db.delete(label)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
