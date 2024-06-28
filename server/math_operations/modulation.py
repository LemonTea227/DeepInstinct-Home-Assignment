from math_operation import MathOperation


class Modulation(MathOperation):
    def operate(self, a: int | float, b: int | float) -> int | float:
        if b == 0:
            raise ValueError("Modulo by zero is undefined.")
        return a % b
