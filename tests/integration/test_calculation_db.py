import pytest
from pydantic import ValidationError
from sqlalchemy.exc import IntegrityError

from app.factory import CalculationFactory
from app.models.calculation import Calculation
from app.models.user import User
from app.schemas.calculation import CalculationCreate
from app.security import hash_password


@pytest.fixture
def user(db):
    user = User(
        username="chima",
        email="chima@example.com",
        password_hash=hash_password("secret123"),
    )
    db.add(user)
    db.commit()
    return user


def save_calculation(db, user_id, a, b, calc_type):
    data = CalculationCreate(a=a, b=b, type=calc_type)
    result = CalculationFactory.create(data.type.value).compute(data.a, data.b)
    calc = Calculation(
        a=data.a, b=data.b, type=data.type.value, result=result, user_id=user_id
    )
    db.add(calc)
    db.commit()
    return calc


@pytest.mark.parametrize(
    "calc_type, result",
    [("Add", 12), ("Sub", 8), ("Multiply", 20), ("Divide", 5)],
)
def test_database_stores_the_computed_result(db, user, calc_type, result):
    save_calculation(db, user.id, 10, 2, calc_type)
    stored = db.query(Calculation).one()
    assert stored.type == calc_type
    assert stored.result == result
    assert stored.user_id == user.id
    assert stored.created_at is not None


def test_calculation_needs_an_existing_user(db):
    with pytest.raises(IntegrityError):
        save_calculation(db, 999, 10, 2, "Add")


def test_deleting_a_user_deletes_their_calculations(db, user):
    save_calculation(db, user.id, 10, 2, "Add")
    save_calculation(db, user.id, 10, 2, "Sub")
    db.delete(user)
    db.commit()
    assert db.query(Calculation).count() == 0


@pytest.mark.parametrize(
    "b, calc_type", [(2, "Power"), (0, "Divide")]
)
def test_bad_input_never_reaches_the_database(db, user, b, calc_type):
    with pytest.raises(ValidationError):
        save_calculation(db, user.id, 10, b, calc_type)
    assert db.query(Calculation).count() == 0
