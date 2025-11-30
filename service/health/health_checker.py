
from abc import ABC, abstractmethod

class HealthChecker(ABC):
    @abstractmethod
    def name(self) -> str:
        """Return the name of the health check component."""
        pass

    @abstractmethod
    def liveness(self) -> bool:
        """Check if the component is alive."""
        pass

    @abstractmethod
    def readiness(self) -> bool:
        """Check if the component is ready to serve traffic."""
        pass
