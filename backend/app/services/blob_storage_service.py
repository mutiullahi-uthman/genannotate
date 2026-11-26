from datetime import timedelta

from google.cloud import storage
from google.cloud.exceptions import NotFound

from app.core.config import settings


class BlobStorageService:
    UPLOAD_URL_TTL = timedelta(minutes=10)
    DOWNLOAD_URL_TTL = timedelta(minutes=5)

    def __init__(self):
        self.client = storage.Client()
        self.bucket = self.client.bucket(settings.GCS_BUCKET_NAME)

    def create_signed_upload_url(
        self,
        object_key: str,
        content_type: str,
    ) -> str:
        return self.bucket.blob(object_key).generate_signed_url(
            version="v4",
            expiration=self.UPLOAD_URL_TTL,
            method="PUT",
            content_type=content_type,
            query_parameters={"ifGenerationMatch": "0"},
        )

    def verify_uploaded_file(
        self,
        object_key: str,
        expected_size: int,
        expected_content_type: str,
    ) -> str | None:
        blob = self.bucket.blob(object_key)
        try:
            blob.reload()
        except NotFound as exc:
            raise ValueError("Uploaded file was not found in storage.") from exc

        if blob.size != expected_size:
            blob.delete()
            raise ValueError("Uploaded file size does not match the declared size.")
        if blob.content_type != expected_content_type:
            blob.delete()
            raise ValueError("Uploaded file content type does not match the declaration.")

        return blob.md5_hash

    def create_signed_download_url(
        self,
        object_key: str,
        download_filename: str,
    ) -> str:
        return self.bucket.blob(object_key).generate_signed_url(
            version="v4",
            expiration=self.DOWNLOAD_URL_TTL,
            method="GET",
            response_disposition=f'attachment; filename="{download_filename}"',
        )

    def delete_file(self, object_key: str) -> None:
        self.bucket.blob(object_key).delete()

    def upload_file(
        self,
        object_key: str,
        file_bytes: bytes,
        content_type: str,
    ) -> None:
        blob = self.bucket.blob(object_key)
        blob.upload_from_string(
            file_bytes,
            content_type=content_type,
        )

    def download_file(
        self,
        object_key: str,
    ) -> bytes:
        blob = self.bucket.blob(object_key)
        return blob.download_as_bytes()
