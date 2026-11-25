from uuid import UUID

from sqlalchemy.orm import Session

from app.models.import_job import ImportJob


class ImportJobRepository:
    def __init__(
        self,
        db: Session,
    ):
        self.db = db

    def create(
        self,
        job: ImportJob,
    ):
        self.db.add(job)
        self.db.commit()
        self.db.refresh(job)

        return job

    def get_by_id(
        self,
        job_id: UUID,
    ):
        return (
            self.db.query(ImportJob)
            .filter(
                ImportJob.id == job_id
            )
            .first()
        )

    def update(
        self,
        job: ImportJob,
    ):
        self.db.commit()
        self.db.refresh(job)

        return job