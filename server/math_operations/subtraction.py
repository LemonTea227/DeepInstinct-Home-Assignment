from math_operation import MathOperation


class Subtraction(MathOperation):
    def operate(self, a: int | float, b: int | float) -> int | float:
        return a - b
