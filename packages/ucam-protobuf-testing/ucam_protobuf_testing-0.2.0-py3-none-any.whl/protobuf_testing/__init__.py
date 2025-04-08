"""
Taken and modified from: https://gist.github.com/mgaitan/dcbe08bf44a5af696f2af752624ac11b
"""

import inspect
from dataclasses import MISSING, Field, is_dataclass
from datetime import datetime
from enum import Enum
from typing import Any, ClassVar, Protocol, get_args, get_origin, runtime_checkable

import factory


@runtime_checkable
class IsDataClass(Protocol):
    __dataclass_fields__: ClassVar[dict[str, Any]]
    __name__: str


def auto_factory(
    target_model: IsDataClass,
    factory_name: str | None = None,
    field_overrides: dict[str, Any] = {},
) -> type[factory.Factory]:
    """Auto factory function to create a factory_boy factory from any dataclass

    Creates a factory_boy factory from the provided dataclass, by reflecting
    defined dataclass fields into suitable equivalent Fakers.

    Usefully, our protobuf auto-generated types are all dataclasses.

    By default `factory_name` is the class name of `target_model` followed by
    "Factory".

    `field_overrides` can be used to provide more specific fakers to a model's
    factory, or to set specific values.
    """

    def get_auto_field(field: Field[Any]) -> factory.Faker | factory.SubFactory:
        if field.default is not MISSING:
            return field.default

        if is_dataclass(field.type) and isinstance(field.type, IsDataClass):
            return factory.SubFactory(auto_factory(field.type))

        if inspect.isclass(field.type) and issubclass(field.type, Enum):
            return factory.Faker("random_element", elements=field.type.__members__.values())

        if field.type is datetime:
            return factory.Faker("date_time_between")

        if (origin := get_origin(field.type)) in [list, tuple, set]:
            args = get_args(field.type)

            return factory.Faker(f"py{origin.__name__}", value_types=args)

        # str, int, float, decimal
        if hasattr(field.type, "__name__"):
            return factory.Faker(f"py{field.type.__name__.lower()}")

        # If we can't work it out, return something! In practice this shouldn't happen
        return factory.Faker("text")

    attrs: dict[str, factory.Faker | factory.SubFactory] = {
        name: get_auto_field(field) for name, field in target_model.__dataclass_fields__.items()
    }

    factory_class = factory.make_factory(target_model, **{**attrs, **field_overrides})
    # Override preset name if provided
    if factory_name:
        factory_class.__name__ = factory_name
    return factory_class
