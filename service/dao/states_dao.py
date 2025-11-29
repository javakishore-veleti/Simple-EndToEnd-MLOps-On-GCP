
import overrides
import os
import time
import logging
import tempfile
import traceback
import pandas as pd
from flask import jsonify
from google.cloud import bigquery, storage
from google.cloud.bigquery import LoadJobConfig, Table
from service.dtos.states import StatesResp, StatesReq
from service.interfaces.daos import StatesDao


LOGGER = logging.getLogger(__name__)

# GCS Config
BUCKET_NAME = "e2e-ml-ops"
PARQUET_FILE_NAME = "states.parquet"


class StatesDaoImpl(StatesDao):
    def __init__(self):
        from service.util.objects import ObjectsFactory
        super().__init__()
        self.table_name = "states_parquet"
        self.table_gcp_uri = f"gs://{BUCKET_NAME}/{PARQUET_FILE_NAME}"
        self.bucket_name = BUCKET_NAME
        self.dataset_id = "e2e_mlops_schema"
        self.job_config: LoadJobConfig = bigquery.LoadJobConfig(
            write_disposition=bigquery.WriteDisposition.WRITE_TRUNCATE,
            source_format=bigquery.SourceFormat.PARQUET
        )
        self.cached_row_count = None
        self.client = ObjectsFactory.get_instance().get_gcp_facade().get_or_create_client()

    # -------------------- SETUP METHOD --------------------
    def setup_cloud_resources(self, resp: StatesResp):
        overall_start = time.time()
        storage_client = storage.Client()

        # Ensure bucket exists
        bucket = storage_client.lookup_bucket(self.bucket_name)
        if bucket is None:
            bucket = storage_client.create_bucket(self.bucket_name, location="US")
            LOGGER.info(f"Bucket {self.bucket_name} created.")
        else:
            LOGGER.info(f"Bucket {self.bucket_name} already exists.")
        resp.add_response_time("create_bucket_time", f"{round(time.time() - overall_start, 3)}s")

        # Ensure Parquet file exists in GCS
        blob = bucket.blob(PARQUET_FILE_NAME)
        local_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), PARQUET_FILE_NAME)
        if not blob.exists() and os.path.exists(local_file_path):
            blob.upload_from_filename(local_file_path)
            LOGGER.info(f"Uploaded {local_file_path} to {self.table_gcp_uri}")
        elif not blob.exists():
            LOGGER.warning("Local Parquet file missing. Run convert_csv_to_parquet first.")

        # Ensure dataset exists
        dataset_ref = f"{self.client.project}.{self.dataset_id}"
        try:
            self.client.get_dataset(dataset_ref)
        except Exception:
            dataset = bigquery.Dataset(dataset_ref)
            dataset.location = "US"
            self.client.create_dataset(dataset, timeout=30)
            LOGGER.info(f"Created dataset {dataset_ref}.")

        resp.add_response_time("setup_cloud_resources_total", f"{round(time.time() - overall_start, 3)}s")
        return "Setup completed successfully."

    # -------------------- UPLOAD PARQUET --------------------
    @overrides.override()
    def upload_parquet(self, req: StatesReq, resp: StatesResp):
        LOGGER.info("Uploading parquet. ENTERED")
        try:
            local_csv_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "states.csv")
            if not os.path.exists(local_csv_path):
                return jsonify({"error": "states.csv not found"}), 400

            # Convert CSV to Parquet
            df = pd.read_csv(local_csv_path)
            parquet_path = os.path.join(tempfile.gettempdir(), PARQUET_FILE_NAME)
            df.to_parquet(parquet_path, engine='pyarrow', index=False)

            # Upload to GCS
            storage_client = storage.Client()
            bucket = storage_client.bucket(BUCKET_NAME)
            bucket.blob(PARQUET_FILE_NAME).upload_from_filename(parquet_path)

            LOGGER.info("Uploading parquet. EXITING with status 200")
            return jsonify({
                "message": "Parquet file uploaded successfully",
                "gcs_uri": self.table_gcp_uri
            }), 200

        except Exception:
            LOGGER.exception("Error during upload_parquet")
            return jsonify({"error": "Internal Server Error"}), 500

    # -------------------- FETCH METHOD --------------------
    @overrides.override
    def find_all(self, req: StatesReq, resp: StatesResp, force_reload=False) -> int:
        overall_start = time.time()
        table_id = f"{self.client.project}.{self.dataset_id}.{self.table_name}"

        # Use cached row count if available and no force reload
        if self.cached_row_count is not None and not force_reload:
            resp.row_count = self.cached_row_count
            resp.add_response_time("fetch_row_count_time", "0.001s")
            resp.add_response_time("find_all_total", f"{round(time.time() - overall_start, 3)}s")
            return resp.row_count

        # Check if table exists
        try:
            destination_table = self.client.get_table(table_id)
            if destination_table.num_rows > 0 and not force_reload:
                self.determine_row_count(destination_table)
                resp.row_count = self.cached_row_count
                resp.add_response_time("fetch_row_count_time", f"{round(time.time() - overall_start, 3)}s")
                resp.add_response_time("find_all_total", f"{round(time.time() - overall_start, 3)}s")
                return resp.row_count
        except Exception:
            LOGGER.info("Table missing or reload requested. Loading from Parquet.")

        # Load table from Parquet in GCS
        start_load = time.time()
        load_job = self.client.load_table_from_uri(self.table_gcp_uri, table_id, job_config=self.job_config)
        load_job.result()
        resp.add_response_time("load_table_time", f"{round(time.time() - start_load, 3)}s")

        # Fetch row count after load
        destination_table = self.client.get_table(table_id)
        self.determine_row_count(destination_table)
        resp.row_count = self.cached_row_count
        resp.add_response_time("fetch_row_count_time", f"{round(time.time() - start_load, 3)}s")
        resp.add_response_time("find_all_total", f"{round(time.time() - overall_start, 3)}s")

        return resp.row_count

    def determine_row_count(self, destination_table: Table):
        self.cached_row_count = destination_table.num_rows


