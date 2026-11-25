from google.cloud import storage

from app.core.config import settings


class BlobStorageService:
    def __init__(self):
        self.client = storage.Client()
        self.bucket = self.client.bucket(settings.GCS_BUCKET_NAME)

    def upload_file(
        self,
        file_name: str,
        file_bytes: bytes,
    ):
        blob = self.bucket.blob(file_name)
        blob.upload_from_string(file_bytes)
        return blob.public_url

    def download_file(
        self,
        file_name: str,
    ) -> bytes:
        blob = self.bucket.blob(file_name)
        return blob.download_as_bytes()
