
from health.health_checker import HealthChecker
from health.health_facade import HealthFacade
from google.cloud import bigquery, storage
import logging

LOGGER = logging.getLogger(__name__)

class MongoDBHealthChecker(HealthChecker):

    def __init__(self):
        pass
