import unittest
from unittest.mock import Mock, patch

from app.services.blob_storage_service import BlobStorageService


class BlobStorageServiceTests(unittest.TestCase):
    def setUp(self):
        self.bucket = Mock()
        self.client = Mock()
        self.client.bucket.return_value = self.bucket
        self.client_patch = patch(
            "app.services.blob_storage_service.storage.Client",
            return_value=self.client,
        )
        self.client_patch.start()
        self.addCleanup(self.client_patch.stop)
        self.service = BlobStorageService()

    def test_creates_a_short_lived_non_overwriting_put_url(self):
        blob = self.bucket.blob.return_value
        blob.generate_signed_url.return_value = "https://signed.example/upload"

        signed_url = self.service.create_signed_upload_url(
            "projects/p/datasets/d/file.csv",
            "text/csv",
        )

        self.assertEqual(signed_url, "https://signed.example/upload")
        blob.generate_signed_url.assert_called_once_with(
            version="v4",
            expiration=self.service.UPLOAD_URL_TTL,
            method="PUT",
            content_type="text/csv",
            query_parameters={"ifGenerationMatch": "0"},
        )

    def test_verifies_uploaded_size_and_content_type(self):
        blob = self.bucket.blob.return_value
        blob.size = 10
        blob.content_type = "text/csv"
        blob.md5_hash = "checksum"

        checksum = self.service.verify_uploaded_file(
            "projects/p/datasets/d/file.csv",
            expected_size=10,
            expected_content_type="text/csv",
        )

        self.assertEqual(checksum, "checksum")
        blob.reload.assert_called_once_with()
        blob.delete.assert_not_called()

    def test_deletes_upload_when_declared_size_does_not_match(self):
        blob = self.bucket.blob.return_value
        blob.size = 11
        blob.content_type = "text/csv"

        with self.assertRaisesRegex(ValueError, "size does not match"):
            self.service.verify_uploaded_file(
                "projects/p/datasets/d/file.csv",
                expected_size=10,
                expected_content_type="text/csv",
            )

        blob.delete.assert_called_once_with()


if __name__ == "__main__":
    unittest.main()
