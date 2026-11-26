from fastapi import HTTPException

from app.core.enums import (
    AssignmentType,
    RecordState,
    UserRole,
    UserStatus,
)

from app.core.enums import (
    AuditAction,
    AuditEntity,
)
from app.models.assignment import Assignment
from app.models.project import ProjectMembership
from app.models.user import User

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
        self._validate_assignee(assignee_id)
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
            commit=False,
        )

        self.db.commit()
        self.db.refresh(created_assignment)
        return created_assignment

    def assign_records_manually(
        self,
        record_ids,
        assignee_id,
        assigned_by_id,
    ):
        self._validate_assignee(assignee_id)
        if len(set(record_ids)) != len(record_ids):
            raise HTTPException(
                status_code=422,
                detail="Record IDs must be unique.",
            )
        records = [
            self.repository.get_record(record_id)
            for record_id in record_ids
        ]
        if any(record is None for record in records):
            raise HTTPException(
                status_code=404,
                detail="One or more records were not found.",
            )

        assignments = []
        for record in records:
            previous_assignee = record.assignee_id
            record.assignee_id = assignee_id
            record.state = RecordState.ASSIGNED
            assignment = Assignment(
                record_id=record.id,
                old_assignee_id=previous_assignee,
                new_assignee_id=assignee_id,
                assigned_by_id=assigned_by_id,
                assignment_type=AssignmentType.MANUAL,
            )
            assignments.append(self.repository.create(assignment))
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
                after_value={"assignee_id": str(assignee_id)},
                commit=False,
            )

        self.db.commit()
        return assignments

    def bulk_assign(
        self,
        dataset_id,
        dataset_version_id,
        assignee_ids,
        assigned_by_id,
        limit,
    ):
        if not assignee_ids:
            raise HTTPException(
                status_code=422,
                detail="Select at least one annotator.",
            )
        if len(set(assignee_ids)) != len(assignee_ids):
            raise HTTPException(
                status_code=422,
                detail="Annotator IDs must be unique.",
            )
        self._validate_assignees(assignee_ids)
        records = (
            self.repository
            .get_unassigned_records(
                dataset_id,
                dataset_version_id,
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
                commit=False,
            )

            assignments.append(
                assignment
            )

        self.db.commit()
        return assignments

    def reassign(
        self,
        record_ids,
        new_assignee_id,
        assigned_by_id,
    ):
        self._validate_assignee(new_assignee_id)
        if len(set(record_ids)) != len(record_ids):
            raise HTTPException(
                status_code=422,
                detail="Record IDs must be unique.",
            )
        result = []
        records = [
            self.repository.get_record(record_id)
            for record_id in record_ids
        ]
        if any(record is None for record in records):
            raise HTTPException(
                status_code=404,
                detail="One or more records were not found.",
            )

        for record in records:
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
            record.state = RecordState.ASSIGNED

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
                commit=False,
            )

            result.append(assignment)

        self.db.commit()
        return result

    def _validate_assignees(self, assignee_ids):
        project_id = self.db.info.get("project_id")
        memberships = (
            self.db.query(ProjectMembership)
            .join(User, User.id == ProjectMembership.user_id)
            .filter(
                ProjectMembership.project_id == project_id,
                ProjectMembership.user_id.in_(assignee_ids),
                ProjectMembership.active.is_(True),
                ProjectMembership.role == UserRole.ANNOTATOR,
                User.status == UserStatus.ACTIVE,
            )
            .all()
        )
        if {membership.user_id for membership in memberships} != set(
            assignee_ids
        ):
            raise HTTPException(
                status_code=422,
                detail="Every assignee must be an active annotator in this project.",
            )

    def _validate_assignee(self, assignee_id):
        self._validate_assignees([assignee_id])
