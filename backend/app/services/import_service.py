from app.models.record import Record
from app.services.import_file_service import (
    ImportFileService,
    ParsedImportFile,
)
from app.services.validation_service import ValidationService


class ImportService:
    def __init__(self, import_file_service=None):
        self.import_file_service = (
            import_file_service or ImportFileService()
        )

    def import_dataset(
        self,
        import_job,
        db,
        parsed_file: ParsedImportFile | None = None,
    ):
        if parsed_file is None:
            parsed_file = self.import_file_service.read_job_file(
                import_job,
                db,
            )

        validation = ValidationService(
            self.import_file_service
        ).validate_parsed_file(
            parsed_file,
            job=import_job,
        )
        if validation.errors:
            raise ValueError(
                "Import file failed validation: "
                + "; ".join(validation.errors)
            )

        records = []

        for row in parsed_file.rows:
            record = Record(
                dataset_id=import_job.dataset_id,
                record_id=row["record_id"],
                language=row["language"],
                instrument=row["instrument"],
                item_id=row["item_id"],
                item_text=row.get("item_text"),
                transcript=row["transcript"],
                audio_link=row.get("audio_link"),
            )

            records.append(record)

        db.add_all(records)

        return len(records)