from service.dao.gcp_facade import GcpFacade
from service.dao.states_dao import StatesDaoImpl
from service.health.health_facade import HealthFacade
from service.health.mlflow_health_checker import MLFlowHealthChecker
from service.health.mongodb_health_checker import MongoDBHealthChecker
from service.interfaces.daos import StatesDao
import os

class ObjectsFactory:
    _instance = None  # class-level variable to hold the singleton instance

    def __init__(self):
        self.states_dao:StatesDao = None
        self.gcp_facade:GcpFacade = None
        self.health_facade:HealthFacade = None

    def initialize(self):
        self.gcp_facade = GcpFacade()
        self.states_dao = StatesDaoImpl()
        self.health_facade = HealthFacade()

        if os.getenv("ENABLE_MONGODB_HEALTH", "false").lower() == "true":
            MongoDBHealthChecker()
        if os.getenv("ENABLE_MLFLOW_HEALTH", "false").lower() == "true":
            MLFlowHealthChecker()

    def get_states_dao(self) -> StatesDao:
        return self.states_dao

    def get_gcp_facade(self) -> GcpFacade:
        return self.gcp_facade

    def get_health_facade(self) -> HealthFacade:
        return self.health_facade

    @classmethod
    def get_instance(cls) -> "ObjectsFactory":
        if cls._instance is None:
            cls._instance = ObjectsFactory()
            cls._instance.initialize()
        return cls._instance