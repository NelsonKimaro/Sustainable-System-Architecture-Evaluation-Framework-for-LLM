from abc import ABC, abstractmethod

class CarbonModel(ABC):
    @abstractmethod
    def calculate_carbon(self) -> float:
        pass
