from fastapi import HTTPException

from app.core.enums import (
    AssignmentType,
    RecordState,
)

from app.core.enums import (
    AuditAction,
    AuditEntity,
)
from app.models.assignment import Assignment

from app.repositories.assignment_repository import (
    AssignmentRepository,
)
from app.repositories.audit_repository import (
    AuditRepository,
)
from app.services.audit_service import (
    AuditService,
)


class AssignmentService:
    def __init__(
        self,
        repository: AssignmentRepository,
        db=None,
    ):
        self.repository = repository
        self.db = db or repository.db
        self.audit_service = AuditService(
            AuditRepository(self.db)
        )

    def assign_record(
        self,
        record_id,
        assignee_id,
        assigned_by_id,
    ):
        record = (
            self.repository.get_record(
                record_id
            )
        )

        if not record:
            raise HTTPException(
                status_code=404,
                detail="Record not found",
            )

        previous_assignee = (
            record.assignee_id
        )

        record.assignee_id = assignee_id

        record.state = (
            RecordState.ASSIGNED
        )

        self.repository.update_record(
            record
        )

        assignment = Assignment(
            record_id=record.id,
            old_assignee_id=(
                previous_assignee
            ),
            new_assignee_id=assignee_id,
            assigned_by_id=assigned_by_id,
            assignment_type=(
                AssignmentType.MANUAL
            ),
        )

        created_assignment = self.repository.create(
            assignment
        )

        self.audit_service.log(
            actor_id=assigned_by_id,
            entity_type=AuditEntity.RECORD,
            entity_id=record.id,
            action=AuditAction.ASSIGN,
            before_value={
                "assignee_id": (
                    str(previous_assignee)
                    if previous_assignee
                    else None
                ),
            },
            after_value={
                "assignee_id": str(assignee_id),
            },
        )

        return created_assignment

    def bulk_assign(
        self,
        dataset_id,
        assignee_ids,
        assigned_by_id,
        limit,
    ):
        records = (
            self.repository
            .get_unassigned_records(
                dataset_id,
                limit,
            )
        )

        assignments = []

        for index, record in enumerate(
            records
        ):
            assignee = assignee_ids[
                index % len(assignee_ids)
            ]

            record.assignee_id = assignee

            record.state = (
                RecordState.ASSIGNED
            )

            self.repository.update_record(
                record
            )

            assignment = Assignment(
                record_id=record.id,
                old_assignee_id=None,
                new_assignee_id=assignee,
                assigned_by_id=assigned_by_id,
                assignment_type=AssignmentType.BULK,
            )

            self.repository.create(
                assignment
            )

            self.audit_service.log(
                actor_id=assigned_by_id,
                entity_type=AuditEntity.RECORD,
                entity_id=record.id,
                action=AuditAction.ASSIGN,
                after_value={
                    "assignee_id": str(assignee),
                },
            )

            assignments.append(
                assignment
            )

        return assignments

    def reassign(
        self,
        record_ids,
        new_assignee_id,
        assigned_by_id,
    ):
        result = []

        for record_id in record_ids:
            record = (
                self.repository.get_record(
                    record_id
                )
            )

            if not record:
                continue

            previous_assignee = record.assignee_id

            assignment = Assignment(
                record_id=record.id,
                old_assignee_id=(
                    record.assignee_id
                ),
                new_assignee_id=(
                    new_assignee_id
                ),
                assigned_by_id=(
                    assigned_by_id
                ),
                assignment_type=(
                    AssignmentType.REASSIGNMENT
                ),
            )

            record.assignee_id = (
                new_assignee_id
            )

            self.repository.update_record(
                record
            )

            self.repository.create(
                assignment
            )

            self.audit_service.log(
                actor_id=assigned_by_id,
                entity_type=AuditEntity.RECORD,
                entity_id=record.id,
                action=AuditAction.REASSIGN,
                before_value={
                    "assignee_id": (
                        str(previous_assignee)
                        if previous_assignee
                        else None
                    ),
                },
                after_value={
                    "assignee_id": str(new_assignee_id),
                },
            )

            result.append(assignment)

        return result
