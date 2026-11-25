from uuid import UUID

from sqlalchemy.orm import Session

from app.models.annotation import Annotation


class AnnotationRepository:
    def __init__(
        self,
        db: Session,
    ):
        self.db = db

    def create(
        self,
        annotation: Annotation,
    ):
        self.db.add(annotation)
        self.db.commit()
        self.db.refresh(annotation)

        return annotation

    def get_latest_for_record(
        self,
        record_id: UUID,
    ):
        return (
            self.db.query(Annotation)
            .filter(
                Annotation.record_id
                == record_id,

                Annotation.is_latest.is_(True),
            )
            .first()
        )

    def update(
        self,
        annotation: Annotation,
    ):
        self.db.commit()
        self.db.refresh(annotation)

        return annotation