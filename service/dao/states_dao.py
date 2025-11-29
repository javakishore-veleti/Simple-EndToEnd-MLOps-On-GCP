import overrides
from google.cloud.bigquery import LoadJobConfig

from service.dtos.states import StatesResp, StatesReq
from service.interfaces.daos import StatesDao
from google.cloud import bigquery
import os
import logging

LOGGER = logging.getLogger(__name__)

# noinspection PyMethodMayBeStatic,PyMissingConstructor,PyTypeChecker
class StatesDaoImpl(StatesDao):

    def __init__(self):
        self.table_name = "e2e_mlops_schema.states"
        self.table_gcp_uri = "gs://e2e-ml-ops/states.csv"
        self.job_config:LoadJobConfig= None

    def load_job_config(self):
        LOGGER.info("Entered")
        if self.job_config is None:
            self.job_config = bigquery.LoadJobConfig(write_disposition=bigquery.WriteDisposition.WRITE_TRUNCATE,
                                                source_format=bigquery.SourceFormat.CSV,
                                                skip_leading_rows=1,)
            self.table_gcp_uri = os.environ.get("E2E_ML_OPS_APP_GCP_URI_FOR_STATES+_CSV", "gs://e2e-ml-ops/states.csv")

        LOGGER.info("Exiting")
        return self.job_config

    def load_table_from_gcp(self):
        from service.util.objects import ObjectsFactory  # Lazy import here
        load_job = ObjectsFactory.get_instance().get_gcp_facade().get_or_create_client().load_table_from_uri(self.table_gcp_uri, self.table_name, job_config=self.job_config)

    @overrides.override
    def find_all(self, req: StatesReq, resp: StatesResp) -> int:
        LOGGER.info("Entered")

        self.load_job_config()

        LOGGER.info("Exiting")
        return 100