import importlib.util
import unittest
from io import BytesIO
from types import SimpleNamespace
from uuid import uuid4

from app.services.import_file_service import (
    ImportFileError,
    ImportFileService,
    parse_import_file,
)


class ImportFileParsingTests(unittest.TestCase):
    def test_parses_csv_headers_and_utf8_bom(self):
        contents = (
            "\ufeffRecord_ID,Language,Instrument,Item_ID,"
            "Verified_Transcript\r\n"
            "r-1,ENGLISH,survey,q-1,Hello\r\n"
        ).encode("utf-8")

        parsed = parse_import_file("records.csv", contents)

        self.assertEqual(
            parsed.columns,
            (
                "record_id",
                "language",
                "instrument",
                "item_id",
                "transcript",
            ),
        )
        self.assertEqual(parsed.rows[0]["transcript"], "Hello")
        self.assertEqual(parsed.row_numbers, (2,))

    def test_rejects_csv_rows_with_extra_values(self):
        contents = (
            "record_id,language\n"
            "r-1,ENGLISH,unexpected\n"
        ).encode("utf-8")

        with self.assertRaisesRegex(
            ImportFileError,
            "Row 2 has more values than the header",
        ):
            parse_import_file("records.csv", contents)

    def test_parses_json_array_of_records(self):
        contents = b'[{"record_id":"r-1","language":"ENGLISH"}]'

        parsed = parse_import_file("records.json", contents)

        self.assertEqual(
            parsed.columns,
            ("record_id", "language"),
        )
        self.assertEqual(parsed.row_numbers, (1,))
        self.assertEqual(parsed.rows[0]["record_id"], "r-1")

    def test_rejects_json_that_is_not_an_array_of_objects(self):
        with self.assertRaisesRegex(
            ImportFileError,
            "array of record objects",
        ):
            parse_import_file("records.json", b'{"record_id":"r-1"}')

    def test_rejects_json_columns_that_normalize_to_duplicates(self):
        contents = (
            b'[{"record_id":"r-1","Record_ID":"r-2"}]'
        )

        with self.assertRaisesRegex(
            ImportFileError,
            "duplicate column names",
        ):
            parse_import_file("records.json", contents)

    def test_rejects_malformed_json_with_location(self):
        with self.assertRaisesRegex(
            ImportFileError,
            "Invalid JSON at line 1, column",
        ):
            parse_import_file("records.json", b"{")

    def test_rejects_unsupported_extensions(self):
        with self.assertRaisesRegex(
            ImportFileError,
            "Unsupported file type",
        ):
            parse_import_file("records.txt", b"")

    @unittest.skipUnless(
        importlib.util.find_spec("openpyxl"),
        "openpyxl is installed in the backend image",
    )
    def test_parses_xlsx_first_sheet(self):
        from openpyxl import Workbook

        workbook = Workbook()
        worksheet = workbook.active
        worksheet.append(
            [
                "record_id",
                "language",
                "instrument",
                "item_id",
                "verified_transcript",
            ]
        )
        worksheet.append(
            ["r-1", "ENGLISH", "survey", "q-1", "Hello"]
        )

        output = BytesIO()
        workbook.save(output)
        workbook.close()

        parsed = parse_import_file("records.xlsx", output.getvalue())

        self.assertEqual(parsed.rows[0]["transcript"], "Hello")
        self.assertEqual(parsed.row_numbers, (2,))


@unittest.skipUnless(
    importlib.util.find_spec("sqlalchemy"),
    "SQLAlchemy is installed in the backend image",
)
class ImportFileServiceTests(unittest.TestCase):
    def test_reads_job_file_from_blob_storage(self):
        dataset_file = SimpleNamespace(
            dataset_id=uuid4(),
            file_name="records.csv",
            object_key="projects/project-id/datasets/dataset-id/records.csv",
            upload_complete=True,
        )

        class QueryStub:
            def filter(self, expression):
                return self

            def first(self):
                return dataset_file

        class DatabaseStub:
            def query(self, model):
                return QueryStub()

        class BlobStorageStub:
            def __init__(self):
                self.requested_path = None

            def download_file(self, path):
                self.requested_path = path
                return (
                    b"record_id,language,instrument,item_id,transcript\n"
                    b"r-1,ENGLISH,survey,q-1,Hello\n"
                )

        storage = BlobStorageStub()
        service = ImportFileService(blob_storage=storage)
        job = SimpleNamespace(
            dataset_id=dataset_file.dataset_id,
            dataset_file_id=uuid4(),
        )

        parsed = service.read_job_file(job, DatabaseStub())

        self.assertEqual(
            storage.requested_path,
            dataset_file.object_key,
        )
        self.assertEqual(parsed.rows[0]["record_id"], "r-1")

    def test_reports_a_missing_source_file(self):
        class QueryStub:
            def filter(self, expression):
                return self

            def first(self):
                return None

        class DatabaseStub:
            def query(self, model):
                return QueryStub()

        service = ImportFileService(blob_storage=object())
        job = SimpleNamespace(
            dataset_id=uuid4(),
            dataset_file_id=uuid4(),
        )

        with self.assertRaisesRegex(
            ImportFileError,
            "source file was not found",
        ):
            service.read_job_file(job, DatabaseStub())

    def test_rejects_a_source_file_from_another_dataset(self):
        dataset_file = SimpleNamespace(
            dataset_id=uuid4(),
            file_name="records.csv",
            object_key="projects/project-id/datasets/other-dataset/records.csv",
            upload_complete=True,
        )

        class QueryStub:
            def filter(self, expression):
                return self

            def first(self):
                return dataset_file

        class DatabaseStub:
            def query(self, model):
                return QueryStub()

        service = ImportFileService(blob_storage=object())
        job = SimpleNamespace(
            dataset_id=uuid4(),
            dataset_file_id=uuid4(),
        )

        with self.assertRaisesRegex(
            ImportFileError,
            "does not belong to this dataset",
        ):
            service.read_job_file(job, DatabaseStub())


if __name__ == "__main__":
    unittest.main()
