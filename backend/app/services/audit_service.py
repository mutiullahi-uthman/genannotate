from app.models.audit_event import AuditEvent

from app.repositories.audit_repository import (
    AuditRepository,
)


class AuditService:
    def __init__(
        self,
        repository: AuditRepository,
    ):
        self.repository = repository

    def log(
        self,
        actor_id,
        entity_type,
        entity_id,
        action,
        before_value=None,
        after_value=None,
        reason=None,
        ip_address=None,
        user_agent=None,
    ):
        audit = AuditEvent(
            actor_id=actor_id,
            entity_type=entity_type,
            entity_id=str(entity_id),
            action=action,
            before_value=before_value,
            after_value=after_value,
            reason=reason,
            ip_address=ip_address,
            user_agent=user_agent,
        )

        return self.repository.create(
            audit
        )

    def list_events(
        self,
        limit: int = 100,
    ):
        return (
            self.repository.list_events(
                limit=limit
            )
        )

    def entity_history(
        self,
        entity_type,
        entity_id,
    ):
        return (
            self.repository.get_entity_events(
                entity_type,
                entity_id,
            )
        )