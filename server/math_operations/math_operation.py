from abc import ABC, abstractmethod


class MathOperation(ABC):
    @abstractmethod
    def operate(self, a: int | float, b: int | float) -> int | float:
        pass
