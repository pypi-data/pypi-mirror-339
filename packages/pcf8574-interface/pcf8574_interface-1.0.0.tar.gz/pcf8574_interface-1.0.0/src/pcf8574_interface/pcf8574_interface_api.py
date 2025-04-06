from abc import ABC, abstractmethod
from typing import List, Optional


class PCF8574InterfaceApi(ABC):
    @abstractmethod
    def notify_clients(
            self,
            unspoiled_values: List[bool],
            override_values: List[Optional[bool]],
            i2c_bus: int,
            i2c_address: int
    ) -> None:
        """
        Implement a method that notifies all connected api-clients with the current port state.
        """
        pass
