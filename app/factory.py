from app.operations import add, divide, multiply, subtract


class AddOperation:
    def compute(self, a: float, b: float) -> float:
        return add(a, b)


class SubOperation:
    def compute(self, a: float, b: float) -> float:
        return subtract(a, b)


class MultiplyOperation:
    def compute(self, a: float, b: float) -> float:
        return multiply(a, b)


class DivideOperation:
    def compute(self, a: float, b: float) -> float:
        return divide(a, b)


class CalculationFactory:
    operations = {
        "Add": AddOperation,
        "Sub": SubOperation,
        "Multiply": MultiplyOperation,
        "Divide": DivideOperation,
    }

    @classmethod
    def create(cls, calc_type: str):
        if calc_type not in cls.operations:
            raise ValueError(f"Unknown calculation type: {calc_type}")
        return cls.operations[calc_type]()
