from google.cloud import bigquery
from google.cloud.bigquery import Client


# noinspection PyMethodMayBeStatic
class GcpFacade:

    def get_or_create_client(self) -> Client:
        client = bigquery.Client()
        return client