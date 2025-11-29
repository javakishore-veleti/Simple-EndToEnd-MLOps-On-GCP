from service.dao.states_dao import StatesDaoImpl
from service.interfaces.daos import StatesDao


class ObjectsFactory:

    def __init__(self):
        self.states_dao:StatesDao = None

    def initialize(self):
        self.states_dao = StatesDaoImpl()

    def get_states_dao(self) -> StatesDao:
        return self.states_dao