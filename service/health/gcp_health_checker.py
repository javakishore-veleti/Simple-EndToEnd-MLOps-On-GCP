
from service.health.health_checker import HealthChecker
from service.health.health_facade import HealthFacade
from google.cloud import bigquery, storage
import logging

LOGGER = logging.getLogger(__name__)

class GCPHealthChecker(HealthChecker):
    def __init__(self):
        LOGGER.info("Initializing GCP Health Checker STARTED")

        self.bigquery_client = bigquery.Client()
        self.storage_client = storage.Client()
        HealthFacade.get_instance().register(self)  # Auto-register

        LOGGER.info("Initializing GCP Health Checker COMPLETE")

    def name(self):
        return "GCP"

    def liveness(self):
        LOGGER.info("GCPHealthChecker.liveness Entered")

        try:
            _ = bigquery.Client()
            _ = storage.Client()

            LOGGER.info("GCPHealthChecker.liveness Exiting True")
            return True
        except Exception:
            LOGGER.info("GCPHealthChecker.liveness Exiting False")
            return False

    def readiness(self):
        LOGGER.info("GCPHealthChecker.readiness Entered")

        try:
            list(self.bigquery_client.list_datasets())
            list(self.storage_client.list_buckets())

            LOGGER.info("GCPHealthChecker.readiness Exiting True")
            return True
        except Exception:
            LOGGER.info("GCPHealthChecker.readiness Exiting False")
            return False
