from service.dtos.states import StatesResp, StatesReq


# noinspection PyMethodMayBeStatic
class StatesDao:

    def __init__(self):
        pass

    def find_all(self, req:StatesReq, resp:StatesResp) -> int:
        raise Exception("Interface Not Implemented Error")

    def setup_cloud_resources(self, resp):
        raise Exception("Interface Not Implemented Error")

    def convert_csv_to_parquet(self, req, resp):
        raise Exception("Interface Not Implemented Error")

    def upload_parquet(self, req: StatesReq, resp: StatesResp):
        raise Exception("Interface Not Implemented Error")