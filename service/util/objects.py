from service.dao.gcp_facade import GcpFacade
from service.dao.states_dao import StatesDaoImpl
from service.interfaces.daos import StatesDao


class ObjectsFactory:
    _instance = None  # class-level variable to hold the singleton instance

    def __init__(self):
        self.states_dao:StatesDao = None
        self.gcp_facade:GcpFacade = None

    def initialize(self):
        self.gcp_facade = GcpFacade()
        self.states_dao = StatesDaoImpl()


    def get_states_dao(self) -> StatesDao:
        return self.states_dao

    def get_gcp_facade(self) -> GcpFacade:
        return self.gcp_facade

    @classmethod
    def get_instance(cls) -> "ObjectsFactory":
        if cls._instance is None:
            cls._instance = ObjectsFactory()
            cls._instance.initialize()
        return cls._instance