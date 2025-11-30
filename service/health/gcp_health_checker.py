
from health.health_checker import HealthChecker
from health.health_facade import HealthFacade
from google.cloud import bigquery, storage
import logging

LOGGER = logging.getLogger(__name__)

class GCPHealthChecker(HealthChecker):
    def __init__(self):
        self.bigquery_client = bigquery.Client()
        self.storage_client = storage.Client()
        HealthFacade.get_instance().register(self)  # Auto-register

    def name(self):
        return "GCP"

    def liveness(self):
        try:
            _ = bigquery.Client()
            _ = storage.Client()
            return True
        except Exception:
            return False

    def readiness(self):
        try:
            list(self.bigquery_client.list_datasets())
            list(self.storage_client.list_buckets())
            return True
        except Exception:
            return False
