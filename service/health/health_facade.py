import logging

LOGGER = logging.getLogger(__name__)

class HealthFacade:
    _instance = None

    def __init__(self):
        LOGGER.info("HealthFacade.__init__ Entered")
        if HealthFacade._instance is not None:
            raise Exception("Use HealthFacade.get_instance()")
        self.checkers = []
        HealthFacade._instance = self
        LOGGER.info("HealthFacade.__init__ Exiting")

    @staticmethod
    def get_instance():
        if HealthFacade._instance is None:
            HealthFacade()
        return HealthFacade._instance

    def register(self, checker):
        LOGGER.info("HealthFacade.register Entered")
        self.checkers.append(checker)

    def liveness(self):
        LOGGER.info("HealthFacade.liveness Entered")
        return {c.name(): "ok" if c.liveness() else "fail" for c in self.checkers}

    def readiness(self):
        LOGGER.info("HealthFacade.readiness Entered")
        return {c.name(): "ok" if c.readiness() else "fail" for c in self.checkers}

    def overall_status(self):
        LOGGER.info("HealthFacade.overall_status Entered")

        ready = self.readiness()
        resp = {
            "status": "ok" if all(v == "ok" for v in ready.values()) else "fail",
            "liveness": self.liveness(),
            "readiness": ready
        }

        LOGGER.info(f"HealthFacade.overall_status Exiting resp {resp}")
        return resp
