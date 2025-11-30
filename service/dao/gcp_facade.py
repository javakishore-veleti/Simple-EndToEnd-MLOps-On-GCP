import os
import json
from google.cloud import bigquery
from google.cloud import storage
from google.cloud.bigquery import Client


class GcpFacade:
    def __init__(self):
        # Decide source based on ENV variable or config
        self.credentials_source = os.getenv("CREDENTIALS_SOURCE", "local")  # "local" or "gcs"
        self.local_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS", "credentials.json")
        self.gcs_bucket = os.getenv("GCS_BUCKET_NAME", "e2e-ml-ops")
        self.gcs_blob = os.getenv("GCS_CREDENTIALS_FILE", "credentials.json")

    def get_or_create_client(self) -> Client:
        # Load credentials dynamically
        if self.credentials_source == "gcs":
            creds_path = self._download_credentials_from_gcs()
        else:
            creds_path = self.local_path

        # Initialize BigQuery client with explicit credentials
        client = bigquery.Client.from_service_account_json(creds_path)
        return client

    def _download_credentials_from_gcs(self) -> str:
        """Download credentials.json from GCS and return local path."""
        if not self.gcs_bucket:
            raise ValueError("GCS_BUCKET_NAME is not set for GCS credentials source.")

        storage_client = storage.Client()
        bucket = storage_client.bucket(self.gcs_bucket)
        blob = bucket.blob(self.gcs_blob)

        local_temp_path = f"/tmp/{self.gcs_blob}"
        blob.download_to_filename(local_temp_path)
        return local_temp_path
