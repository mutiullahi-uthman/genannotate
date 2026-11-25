import unittest
from types import SimpleNamespace

from app.services.import_file_service import ParsedImportFile
from app.services.import_file_service import ImportFileError
from app.services.validation_service import (
    ValidationService,
)


class DataFrameStub:
    def __init__(self, rows, columns=None):
        self.rows = rows
        self.columns = (
            columns
            if columns is not None
            else tuple(rows[0].keys())
        )

    def to_dict(self, orient):
        if orient != "records":
            raise ValueError(f"Unsupported orientation: {orient}")
        return self.rows


class ValidationServiceTests(unittest.TestCase):
    def setUp(self):
        self.service = ValidationService()

    def test_accepts_complete_rows_with_unique_ids(self):
        dataframe = DataFrameStub(
            [
                {
                    "record_id": "record-1",
                    "language": "ENGLISH",
                    "instrument": "survey",
                    "item_id": "item-1",
                    "transcript": "A response",
                }
            ]
        )

        self.assertEqual(
            self.service.validate_dataframe(dataframe),
            [],
        )

    def test_reports_missing_columns_without_indexing_them(self):
        dataframe = DataFrameStub(
            [],
            columns=("language", "instrument", "item_id", "transcript"),
        )

        self.assertEqual(
            self.service.validate_dataframe(dataframe),
            ["Missing column: record_id"],
        )

    def test_reports_missing_values_by_csv_row(self):
        dataframe = DataFrameStub(
            [
                {
                    "record_id": "record-1",
                    "language": "ENGLISH",
                    "instrument": "survey",
                    "item_id": "item-1",
                    "transcript": "A response",
                },
                {
                    "record_id": "record-2",
                    "language": "ENGLISH",
                    "instrument": "survey",
                    "item_id": "item-2",
                    "transcript": " ",
                },
            ]
        )

        self.assertEqual(
            self.service.validate_dataframe(dataframe),
            ["Row 3: transcript is required"],
        )

    def test_reports_duplicate_record_ids_by_csv_row(self):
        row = {
            "record_id": "record-1",
            "language": "ENGLISH",
            "instrument": "survey",
            "item_id": "item-1",
            "transcript": "A response",
        }
        duplicate = {**row, "record_id": " record-1 "}
        dataframe = DataFrameStub([row, duplicate])

        self.assertEqual(
            self.service.validate_dataframe(dataframe),
            ["Row 3: duplicate record_id 'record-1'"],
        )

    def test_reports_nan_as_a_missing_value(self):
        dataframe = DataFrameStub(
            [
                {
                    "record_id": "record-1",
                    "language": "ENGLISH",
                    "instrument": "survey",
                    "item_id": "item-1",
                    "transcript": float("nan"),
                }
            ]
        )

        self.assertEqual(
            self.service.validate_dataframe(dataframe),
            ["Row 2: transcript is required"],
        )

    def test_validate_job_updates_row_counts(self):
        parsed_file = ParsedImportFile(
            columns=(
                "record_id",
                "language",
                "instrument",
                "item_id",
                "transcript",
            ),
            rows=[
                {
                    "record_id": "record-1",
                    "language": "ENGLISH",
                    "instrument": "survey",
                    "item_id": "item-1",
                    "transcript": "A response",
                },
                {
                    "record_id": "record-1",
                    "language": "ENGLISH",
                    "instrument": "survey",
                    "item_id": "item-2",
                    "transcript": "Another response",
                },
            ],
            row_numbers=(2, 3),
        )

        class FileServiceStub:
            def read_job_file(self, job, db):
                return parsed_file

        job = SimpleNamespace(
            total_rows=0,
            valid_rows=0,
            invalid_rows=0,
        )
        service = ValidationService(
            import_file_service=FileServiceStub()
        )

        result = service.validate_job(job, db=None)

        self.assertEqual(
            result.errors,
            ("Row 3: duplicate record_id 'record-1'",),
        )
        self.assertEqual(
            (job.total_rows, job.valid_rows, job.invalid_rows),
            (2, 1, 1),
        )

    def test_validate_job_returns_source_file_errors(self):
        class FileServiceStub:
            def read_job_file(self, job, db):
                raise ImportFileError(
                    "Unsupported file type. Use CSV, XLSX, or JSON."
                )

        job = SimpleNamespace(
            total_rows=3,
            valid_rows=2,
            invalid_rows=1,
        )
        service = ValidationService(
            import_file_service=FileServiceStub()
        )

        result = service.validate_job(job, db=None)

        self.assertEqual(
            result.errors,
            ("Unsupported file type. Use CSV, XLSX, or JSON.",),
        )
        self.assertIsNone(result.parsed_file)
        self.assertEqual(
            (job.total_rows, job.valid_rows, job.invalid_rows),
            (0, 0, 0),
        )


if __name__ == "__main__":
    unittest.main()
