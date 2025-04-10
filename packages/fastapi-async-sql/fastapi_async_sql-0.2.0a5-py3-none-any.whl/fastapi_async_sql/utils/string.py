"""String utils."""

import re

import inflect


def to_camel(value: str) -> str:
    """Convert snake_case to camelCase.

    Args:
        value (str): snake_case string.

    Returns:
        str: camelCase string.
    """
    return "".join(
        word.capitalize() if idx != 0 else word
        for idx, word in enumerate(value.split("_"))
    )


def to_snake(name: str) -> str:
    """Convert CamelCase to snake_case.

    Args:
        name (str): CamelCase string.

    Returns:
        str: snake_case string.
    """
    name = re.sub("(.)([A-Z][a-z]+)", r"\1_\2", name)
    return re.sub("([a-z0-9])([A-Z])", r"\1_\2", name).lower()


def pluralize_camel(value: str) -> str:
    """Pluralize a CamelCase word.

    Args:
        value (str): CamelCase string.

    Returns:
        str: Pluralized CamelCase string.
    """
    p = inflect.engine()
    name = to_snake(value).split("_")
    return "".join(
        p.plural(word).title() if len(name) == 1 or idx != 0 else word
        for idx, word in enumerate(name)
    )


def to_snake_plural(value: str) -> str:
    """Convert CamelCase to snake_case and pluralize.

    Args:
        value (str): CamelCase string.

    Returns:
        str: snake_case string.
    """
    return to_snake(pluralize_camel(value))
