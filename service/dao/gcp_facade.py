
from google.cloud import bigquery
from google.cloud import storage
import logging

LOGGER = logging.getLogger(__name__)

class GcpFacade:
    def __init__(self):
        # No credential handling needed; Cloud Run uses ADC automatically
        pass

    def get_or_create_client(self) -> bigquery.Client:
        LOGGER.info('get_or_create_client Entered')
        """Return a BigQuery client using Cloud Run's service account."""

        client_obj = bigquery.Client()

        LOGGER.info('get_or_create_client Exiting client_obj')
        return client_obj

    def get_storage_client(self) -> storage.Client:
        LOGGER.info('get_storage_client Entered')

        """Return a GCS client using Cloud Run's service account."""
        client_obj = storage.Client()

        LOGGER.info('get_storage_client Exiting client_obj')
        return client_obj

    def download_blob(self, bucket_name: str, source_blob_name: str, destination_file_name: str):
        LOGGER.info('download_blob Entered')

        """Download a blob from GCS to a local file."""
        storage_client = self.get_storage_client()
        bucket = storage_client.bucket(bucket_name)
        blob = bucket.blob(source_blob_name)
        blob.download_to_filename(destination_file_name)
        print(f"Downloaded {source_blob_name} from bucket {bucket_name} to {destination_file_name}")

        LOGGER.info('download_blob Exiting')
