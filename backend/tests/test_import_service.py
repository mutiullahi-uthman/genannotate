import importlib.util
import unittest
from types import SimpleNamespace
from uuid import uuid4

from app.services.import_file_service import ParsedImportFile


@unittest.skipUnless(
    importlib.util.find_spec("sqlalchemy"),
    "SQLAlchemy is installed in the backend image",
)
class ImportServiceTests(unittest.TestCase):
    def setUp(self):
        from app.services.import_service import ImportService

        self.service = ImportService()
        self.job = SimpleNamespace(dataset_id=uuid4())
        self.dataset_version_id = uuid4()

        class DatabaseStub:
            def __init__(self):
                self.records = None
                self.committed = False

            def add_all(self, records):
                self.records = records

            def commit(self):
                self.committed = True

        self.db = DatabaseStub()

    def test_import_dataset_adds_records_for_the_job_dataset(self):
        parsed_file = ParsedImportFile(
            columns=(
                "record_id",
                "language",
                "instrument",
                "item_id",
                "transcript",
                "item_text",
                "audio_link",
            ),
            rows=[
                {
                    "record_id": "r-1",
                    "language": "ENGLISH",
                    "instrument": "survey",
                    "item_id": "q-1",
                    "transcript": "Hello",
                    "item_text": "Question",
                    "audio_link": "https://example.test/audio",
                }
            ],
            row_numbers=(2,),
        )

        count = self.service.import_dataset(
            import_job=self.job,
            db=self.db,
            dataset_version_id=self.dataset_version_id,
            parsed_file=parsed_file,
        )

        self.assertEqual(count, 1)
        self.assertFalse(self.db.committed)
        self.assertEqual(len(self.db.records), 1)
        self.assertEqual(
            self.db.records[0].dataset_id,
            self.job.dataset_id,
        )
        self.assertEqual(
            self.db.records[0].dataset_version_id,
            self.dataset_version_id,
        )
        self.assertEqual(
            self.db.records[0].record_id,
            "r-1",
        )
        self.assertEqual(
            self.db.records[0].item_text,
            "Question",
        )
        self.assertEqual(
            self.db.records[0].audio_link,
            "https://example.test/audio",
        )

    def test_import_dataset_rejects_invalid_rows_before_writing(self):
        parsed_file = ParsedImportFile(
            columns=("record_id",),
            rows=[{"record_id": "r-1"}],
            row_numbers=(2,),
        )

        with self.assertRaisesRegex(
            ValueError,
            "failed validation",
        ):
            self.service.import_dataset(
                import_job=self.job,
                db=self.db,
                dataset_version_id=self.dataset_version_id,
                parsed_file=parsed_file,
            )

        self.assertIsNone(self.db.records)
        self.assertFalse(self.db.committed)


if __name__ == "__main__":
    unittest.main()
