import pytest

from app.factory import (
    AddOperation,
    CalculationFactory,
    DivideOperation,
    MultiplyOperation,
    SubOperation,
)


@pytest.mark.parametrize(
    "calc_type, expected_class, result",
    [
        ("Add", AddOperation, 12),
        ("Sub", SubOperation, 8),
        ("Multiply", MultiplyOperation, 20),
        ("Divide", DivideOperation, 5),
    ],
)
def test_factory_picks_the_right_operation(calc_type, expected_class, result):
    operation = CalculationFactory.create(calc_type)
    assert isinstance(operation, expected_class)
    assert operation.compute(10, 2) == result


def test_factory_rejects_an_unknown_type():
    with pytest.raises(ValueError, match="Unknown calculation type"):
        CalculationFactory.create("Power")


def test_divide_operation_still_blocks_zero():
    with pytest.raises(ValueError):
        CalculationFactory.create("Divide").compute(10, 0)
