"""Exceptions module."""


class MissingArgsError(Exception):
    """Exception raised when one or more args are not passed as parameter."""

    def __init__(self, *args: str):
        msg = f"You need to pass {' or '.join(args)} parameter."

        super().__init__(msg)


class MultipleArgsError(Exception):
    """Exception raised when the user passes multiple args that are mutually exclusive."""

    def __init__(self, *args: str):
        msg = f"Mutually exclusive parameters: {', '.join(args)}."

        super().__init__(msg)


class ObjectNotFoundError(Exception):
    """Exception raised when an object is not found in the database."""

    def __init__(self, obj: str, **kwargs):
        msg = f"{obj} not found"
        if kwargs:
            msg += f" with {', '.join([f'{k}={v}' for k, v in kwargs.items()])}"
        msg += "."

        super().__init__(msg)


class CreateObjectError(Exception):
    """Exception raised when an object cannot be created in the database."""

    def __init__(self, obj: str, **kwargs):
        msg = f"Error creating {obj}"
        if kwargs:
            msg += f" with {', '.join([f'{k}={v}' for k, v in kwargs.items()])}"
        msg += "."

        super().__init__(msg)
