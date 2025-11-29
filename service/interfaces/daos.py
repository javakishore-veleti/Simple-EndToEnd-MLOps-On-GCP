from service.dtos.states import StatesResp, StatesReq


# noinspection PyMethodMayBeStatic
class StatesDao:

    def __init__(self):
        pass

    def find_all(self, req:StatesReq, resp:StatesResp) -> int:
        raise Exception("Interface Not Implemented Error")