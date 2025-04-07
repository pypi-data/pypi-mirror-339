from typing import Optional

__all__ = [
    "CmdBaseException",
    "NotEnoughArgumentError",
    "NotFoundError",
    "ConversionError",
]


class CmdBaseException(Exception):
    def __init__(self, message: str, *args):
        self.message = message
        self.args = args
        super().__init__(self.message)

    def __str__(self):
        return self.message


class NotEnoughArgumentError(CmdBaseException):
    """Raises when an option is missing an argument.

    Parameters
    ----------
    message : str
        Error message.
    option : str
        Name of the option.
    """

    def __init__(self, message: str, option: str):
        self.message = message
        self.option = option
        super().__init__(message)


class NotFoundError(CmdBaseException):
    """Raises when a command or a command module is not found

    Parameters
    ----------
    message : str
        Error message.
    name : str
        Name of the identifier.
    """

    def __init__(self, message: str, name: Optional[str] = None):
        self.message = message
        if name is not None:
            self.name = name
        else:
            self.name = ""
        super().__init__(message)


class ConversionError(CmdBaseException):
    """Raises when failed to convert an object to a specific type

    Parameters
    ----------
    message : str
        Error message.
    option : str
        Name of the option.
    """

    def __init__(self, message: str, option: str):
        self.option = option
        super().__init__(message)
