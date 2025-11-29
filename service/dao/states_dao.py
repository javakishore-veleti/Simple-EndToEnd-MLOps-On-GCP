import overrides

from service.dtos.states import StatesResp, StatesReq
from service.interfaces.daos import StatesDao


# noinspection PyMethodMayBeStatic,PyMissingConstructor
class StatesDaoImpl(StatesDao):

    def __init__(self):
        pass

    @overrides.override
    def find_all(self, req: StatesReq, resp: StatesResp) -> int:
        return 100