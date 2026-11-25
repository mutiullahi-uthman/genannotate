from fastapi import APIRouter
from fastapi import Depends
from sqlalchemy.orm import Session

from app.core.enums import AuditEntity
from app.core.permissions import ADMIN_ONLY
from app.database.session import get_db

from app.schemas.audit import (
    AuditResponse,
)

from app.repositories.audit_repository import (
    AuditRepository,
)

from app.services.audit_service import (
    AuditService,
)


router = APIRouter(
    prefix="/audits",
    tags=["Audit Trail"],
    dependencies=[Depends(ADMIN_ONLY)],
)

# GET recent audit events
@router.get(
    "",
    response_model=list[AuditResponse],
)
def get_audits(
    limit: int = 100,
    db: Session = Depends(get_db),
):
    service = AuditService(
        AuditRepository(db)
    )

    return service.list_events(
        limit=limit
    )
    
# GET entity history
@router.get(
    "/{entity_type}/{entity_id}",
    response_model=list[AuditResponse],
)
def get_entity_history(
    entity_type: AuditEntity,
    entity_id: str,
    db: Session = Depends(get_db),
):
    service = AuditService(
        AuditRepository(db)
    )

    return service.entity_history(
        entity_type,
        entity_id,
    )    