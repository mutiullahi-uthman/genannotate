import math
from dataclasses import dataclass

from app.services.import_file_service import (
    ImportFileError,
    ImportFileService,
    ParsedImportFile,
)

REQUIRED_COLUMNS = (
    "record_id",
    "language",
    "instrument",
    "item_id",
    "transcript",
)


@dataclass(frozen=True)
class ValidationResult:
    errors: tuple[str, ...]
    parsed_file: ParsedImportFile | None
    total_rows: int
    valid_rows: int
    invalid_rows: int


class ValidationService:
    def __init__(self, import_file_service=None):
        self.import_file_service = (
            import_file_service or ImportFileService()
        )

    def validate_dataframe(
        self,
        dataframe,
    ):
        rows = dataframe.to_dict(orient="records")
        parsed_file = ParsedImportFile(
            columns=tuple(dataframe.columns),
            rows=rows,
            row_numbers=tuple(range(2, len(rows) + 2)),
        )
        return list(
            self.validate_parsed_file(parsed_file).errors
        )

    def validate_job(
        self,
        job,
        db,
        parsed_file: ParsedImportFile | None = None,
    ) -> ValidationResult:
        if parsed_file is None:
            try:
                parsed_file = self.import_file_service.read_job_file(
                    job,
                    db,
                )
            except ImportFileError as exc:
                self._set_job_counts(
                    job,
                    total_rows=0,
                    valid_rows=0,
                    invalid_rows=0,
                )
                return ValidationResult(
                    errors=(str(exc),),
                    parsed_file=None,
                    total_rows=0,
                    valid_rows=0,
                    invalid_rows=0,
                )

        result = self.validate_parsed_file(
            parsed_file,
            job=job,
        )
        return result

    def validate_parsed_file(
        self,
        parsed_file: ParsedImportFile,
        job=None,
    ) -> ValidationResult:
        total_rows = len(parsed_file.rows)
        missing_columns = [
            column
            for column in REQUIRED_COLUMNS
            if column not in parsed_file.columns
        ]
        errors = [
            f"Missing column: {column}"
            for column in missing_columns
        ]

        if not total_rows:
            if not errors:
                errors.append("No data rows found")
            invalid_rows = 0
        elif missing_columns:
            invalid_rows = total_rows
        else:
            row_errors, invalid_row_numbers = self._validate_rows(
                parsed_file
            )
            errors.extend(row_errors)
            invalid_rows = len(invalid_row_numbers)

        valid_rows = total_rows - invalid_rows
        if job is not None:
            self._set_job_counts(
                job,
                total_rows=total_rows,
                valid_rows=valid_rows,
                invalid_rows=invalid_rows,
            )

        return ValidationResult(
            errors=tuple(errors),
            parsed_file=parsed_file,
            total_rows=total_rows,
            valid_rows=valid_rows,
            invalid_rows=invalid_rows,
        )

    def _validate_rows(
        self,
        parsed_file: ParsedImportFile,
    ) -> tuple[list[str], set[int]]:
        errors = []
        invalid_row_numbers = set()
        seen_record_ids = set()

        for row, row_number in zip(
            parsed_file.rows,
            parsed_file.row_numbers,
        ):
            for column in REQUIRED_COLUMNS:
                if self._is_missing(row.get(column)):
                    errors.append(
                        f"Row {row_number}: {column} is required"
                    )
                    invalid_row_numbers.add(row_number)

            record_id = row.get("record_id")
            if self._is_missing(record_id):
                continue

            normalized_record_id = str(record_id).strip()
            if normalized_record_id in seen_record_ids:
                errors.append(
                    f"Row {row_number}: duplicate record_id "
                    f"'{normalized_record_id}'"
                )
                invalid_row_numbers.add(row_number)
            else:
                seen_record_ids.add(normalized_record_id)

        return errors, invalid_row_numbers

    @staticmethod
    def _set_job_counts(
        job,
        total_rows: int,
        valid_rows: int,
        invalid_rows: int,
    ) -> None:
        job.total_rows = total_rows
        job.valid_rows = valid_rows
        job.invalid_rows = invalid_rows

    @staticmethod
    def _is_missing(value) -> bool:
        if value is None:
            return True

        if isinstance(value, str):
            return not value.strip()

        try:
            return math.isnan(value)
        except (OverflowError, TypeError, ValueError):
            return False