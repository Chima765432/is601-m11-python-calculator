from datetime import datetime, timezone

import pytest
from pydantic import ValidationError

from app.models.calculation import Calculation
from app.schemas.calculation import CalculationCreate, CalculationRead


def test_create_accepts_valid_input():
    calc = CalculationCreate(a=10, b=2, type="Divide")
    assert calc.type == "Divide"


@pytest.mark.parametrize("calc_type", ["Power", "add", ""])
def test_create_rejects_unknown_types(calc_type):
    with pytest.raises(ValidationError):
        CalculationCreate(a=10, b=2, type=calc_type)


def test_create_rejects_a_zero_divisor():
    with pytest.raises(ValidationError, match="Cannot divide by zero"):
        CalculationCreate(a=10, b=0, type="Divide")


@pytest.mark.parametrize("calc_type", ["Add", "Sub", "Multiply"])
def test_zero_is_fine_for_other_types(calc_type):
    assert CalculationCreate(a=10, b=0, type=calc_type).b == 0


@pytest.mark.parametrize("a, b", [("ten", 2), (10, None)])
def test_create_rejects_non_numbers(a, b):
    with pytest.raises(ValidationError):
        CalculationCreate(a=a, b=b, type="Add")


def test_create_requires_every_field():
    with pytest.raises(ValidationError):
        CalculationCreate(a=10, b=2)


def test_read_builds_from_a_model():
    calc = Calculation(
        id=1,
        a=10,
        b=2,
        type="Multiply",
        result=20,
        user_id=1,
        created_at=datetime.now(timezone.utc),
    )
    data = CalculationRead.model_validate(calc).model_dump()
    assert data["result"] == 20
    assert data["type"] == "Multiply"
