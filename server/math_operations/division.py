from math_operation import MathOperation


class Division(MathOperation):
    def operate(self, a: int | float, b: int | float) -> int | float:
        if b == 0:
            raise ValueError("Division by zero is undefined.")
        return a / b
