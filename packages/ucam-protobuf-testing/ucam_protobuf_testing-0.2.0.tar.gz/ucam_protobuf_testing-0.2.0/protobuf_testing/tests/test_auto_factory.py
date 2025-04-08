from dataclasses import dataclass
from datetime import datetime
from enum import Enum

import factory
import factory.random
import pytest

from protobuf_testing import auto_factory


@dataclass
class A:
    a_text: str
    integer: int
    value: float


class MyEnum(Enum):
    option1 = 1
    option2 = 2


@dataclass
class B:
    related: A
    an_enum: MyEnum
    list_of_str: list[str]
    my_date: datetime


def test_auto_factory():
    factory.random.reseed_random(121213)

    BFactory = auto_factory(B)

    b = BFactory()

    # Known values from seed, no other good way to test
    assert b.an_enum == MyEnum.option2
    assert b.list_of_str == [
        "vZlJIJCmLSNfZXxraIqr",
        "QGRhNwXoxwSAAYwAHucD",
        "sgKfcOoqTBLEnCrwhPUF",
        "ABBUDcodNYQorGwOtMZB",
        "GcgHocZIeWgpTquDndXw",
        "MLFpfnvDhzwevrVwQsIn",
        "lLYQTvcGDEQvpyiltjFZ",
    ]
    assert b.related.a_text == "MaswdZBYMPmlyvFDdPOM"
    assert b.related.integer == 5034
    assert b.related.value == 82423891125579.4

    assert b.my_date.year == 2006
    assert b.my_date.month == 7
    assert b.my_date.day == 20


def test_auto_factory_name():
    BFactory = auto_factory(B)
    MyBFactory = auto_factory(B, factory_name="MyGreatBFactory")

    assert BFactory.__name__ == "BFactory"
    assert MyBFactory.__name__ == "MyGreatBFactory"


def test_auto_factory_attrs():
    AFactory = auto_factory(
        A,
        field_overrides={"integer": factory.Faker("pyint", min_value=-3, max_value=3)},
    )
    BFactory = auto_factory(
        B,
        field_overrides={"list_of_str": ["my-test-str"], "related": factory.SubFactory(AFactory)},
    )

    b = BFactory()

    assert b.list_of_str == ["my-test-str"]
    assert b.related.integer >= -3
    assert b.related.integer <= 3


def test_auto_factory_unrecognised_attrs():
    AFactory = auto_factory(A, field_overrides={"not_defined": "my-test-str"})

    with pytest.raises(TypeError):
        _ = AFactory()
