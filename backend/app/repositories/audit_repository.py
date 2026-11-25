from sqlalchemy.orm import Session

from app.models.audit_event import AuditEvent


class AuditRepository:
    def __init__(
        self,
        db: Session,
    ):
        self.db = db

    def create(
        self,
        audit: AuditEvent,
    ):
        self.db.add(audit)
        self.db.commit()
        self.db.refresh(audit)

        return audit

    def list_events(
        self,
        limit: int = 100,
    ):
        return (
            self.db.query(AuditEvent)
            .order_by(
                AuditEvent.created_at.desc()
            )
            .limit(limit)
            .all()
        )

    def get_entity_events(
        self,
        entity_type,
        entity_id,
    ):
        return (
            self.db.query(AuditEvent)
            .filter(
                AuditEvent.entity_type
                == entity_type,

                AuditEvent.entity_id
                == str(entity_id),
            )
            .order_by(
                AuditEvent.created_at.desc()
            )
            .all()
        )