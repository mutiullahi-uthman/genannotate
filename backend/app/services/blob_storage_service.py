from azure.storage.blob import BlobServiceClient

from app.core.config import settings


class BlobStorageService:
    def __init__(self):
        self.client = BlobServiceClient.from_connection_string(
            settings.AZURE_STORAGE_CONNECTION_STRING
        )

        self.container = settings.AZURE_STORAGE_CONTAINER

    def upload_file(
        self,
        file_name: str,
        file_bytes: bytes,
    ):
        blob_client = self.client.get_blob_client(
            container=self.container,
            blob=file_name,
        )

        blob_client.upload_blob(
            file_bytes,
            overwrite=True,
        )

        return blob_client.url

    def download_file(
        self,
        file_name: str,
    ) -> bytes:
        blob_client = self.client.get_blob_client(
            container=self.container,
            blob=file_name,
        )

        return blob_client.download_blob().readall()