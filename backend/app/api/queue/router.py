from fastapi import APIRouter
from fastapi import Depends

from sqlalchemy.orm import Session

from app.core.auth import get_current_user

from app.database.session import get_db

from app.services.queue_service import (
    QueueService,
)


router = APIRouter(
    prefix="/queue",
    tags=["Queue"],
)

# GET /queue/my-queue
@router.get("")
def get_queue(
    db: Session = Depends(get_db),
    current_user=Depends(
        get_current_user
    ),
):
    service = QueueService(db)

    return service.get_my_queue(
        current_user.id
    )
    
# GET /queue/next
@router.get("/next")
def get_next_record(
    db: Session = Depends(get_db),
    current_user=Depends(
        get_current_user
    ),
):
    service = QueueService(db)

    return service.get_next_record(
        current_user.id
    )
    
# GET /queue/stats
@router.get("/my-stats")
def get_queue_stats(
    db: Session = Depends(get_db),
    current_user=Depends(
        get_current_user
    ),
):
    service = QueueService(db)

    return service.get_queue_stats(
        current_user.id
    )
    
# GET /queue/start/<record_id>
@router.post(
    "/start/{record_id}"
)
def start_annotation(
    record_id: str,
    db: Session = Depends(get_db),
    current_user=Depends(
        get_current_user
    ),
):
    service = QueueService(db)

    return service.start_annotation(
        record_id=record_id,
        user_id=current_user.id,
    )            