from abc import ABC, abstractmethod
import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG)

logger = logging.getLogger(__name__)


class MathOperation(ABC):
    @abstractmethod
    def operate(self, a: int | float, b: int | float) -> int | float:
        pass


class Addition(MathOperation):
    def operate(self, a: int | float, b: int | float) -> int | float:
        return a + b


class Subtraction(MathOperation):
    def operate(self, a: int | float, b: int | float) -> int | float:
        return a - b


class Multiplication(MathOperation):
    def operate(self, a: int | float, b: int | float) -> int | float:
        return a * b


class Division(MathOperation):
    def operate(self, a: int | float, b: int | float) -> int | float:
        if b == 0:
            raise ValueError("Division by zero is undefined.")
        return a / b


class Power(MathOperation):
    def operate(self, a: int | float, b: int | float) -> int | float:
        return a ** b


class Modulation(MathOperation):
    def operate(self, a: int | float, b: int | float) -> int | float:
        if b == 0:
            raise ValueError("Modulo by zero is undefined.")
        return a % b
