"""Utilities for partial models."""
# https://github.com/pydantic/pydantic/issues/1223
# https://github.com/pydantic/pydantic/pull/3179
# https://github.com/pydantic/pydantic/issues/1673

from collections.abc import Callable, Collection
from copy import deepcopy
from typing import Any, Optional, TypeVar

from pydantic import BaseModel, create_model
from pydantic.fields import FieldInfo

Model = TypeVar("Model", bound=type[BaseModel])


def optional(
    without_fields: Collection[str] | None = None,
) -> Callable[[type[Model]], type[Model]]:
    """A decorator that create a partial model.

    Args:
        without_fields (list[str], optional): Fields to exclude. Defaults to None.

    Returns:
        Type[BaseModel]: ModelBase partial model.
    """
    if without_fields is None:
        without_fields = set()

    def wrapper(model: type[Model]) -> type[Model]:
        base_model: type[Model] = model

        def make_field_optional(
            field: FieldInfo, default: Any = None
        ) -> tuple[Any, FieldInfo]:
            new = deepcopy(field)
            new.default = default
            new.annotation = Optional[field.annotation]  # type: ignore
            return new.annotation, new

        if without_fields:
            base_model = BaseModel  # type: ignore

        return create_model(
            model.__name__,
            __base__=base_model,
            __module__=model.__module__,
            **{
                field_name: make_field_optional(field_info)  # type: ignore
                for field_name, field_info in model.model_fields.items()  # type: ignore
                if field_name not in without_fields
            },
        )

    return wrapper
