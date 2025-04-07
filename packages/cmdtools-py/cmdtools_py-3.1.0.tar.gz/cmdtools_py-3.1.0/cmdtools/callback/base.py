from __future__ import annotations

import inspect
import typing
from typing import Any, Callable, Dict, Optional, Union

try:
    from typing import TypeAlias
except ImportError:
    from typing_extensions import TypeAlias

from cmdtools.callback.option import OptionModifier, Options
from cmdtools.converter.base import BasicTypes
from cmdtools.errors import NotEnoughArgumentError, ConversionError
from cmdtools.ext.param import apply_params

if typing.TYPE_CHECKING:
    from cmdtools import Cmd

__all__ = [
    "Attributes",
    "Context",
    "ErrorContext",
    "Callback",
    "ErrorCallback",
    "callback_init",
    "add_option",
    "AttributeType",
]


class Attributes:
    """An attributes container

    Parameters
    ----------
    attrs : dict
        A dictionary containing any objects.
    """

    def __init__(self, attrs: Optional[Dict[str, Any]] = None):
        if attrs is None:
            self.attrs = {}
        else:
            self.attrs = attrs

    def __getattr__(self, name: str) -> Optional[str]:
        return self.attrs.get(name)


class BaseContext:
    """The base class for context."""

    def __init__(self, command: Cmd, attrs: AttributeType = None):
        self.command = command

        if isinstance(attrs, Attributes):
            self.attrs = attrs
        elif isinstance(attrs, dict):
            self.attrs = Attributes(attrs)
        else:
            self.attrs = Attributes()

AttributeType: TypeAlias = Optional[Union[Attributes, Dict[str, Any]]]

class Context(BaseContext):
    """A context to be passed to a Callback when command is executed.

    Parameters
    ----------
    command : Cmd
        The command object to be executed.
    options : Options
        The options of the callback.
    attrs : AttributeType
        Additional attributes to be passed to the callback context.

    Raises
    ------
    ConversionError
        If converter fails to convert the value of an option.
    """

    def __init__(
        self,
        command: Cmd,
        options: Optional[Options] = None,
        attrs: AttributeType = None,
    ):
        if isinstance(options, Options):
            self.options = options
        elif isinstance(options, dict):
            self.options = Options(options)
        else:
            self.options = Options()

        super().__init__(command, attrs)

        for idx, option in enumerate(self.options.options):
            if option.value is None and option.default is None:
                raise NotEnoughArgumentError(
                    f"Not enough argument for option: {option.name}", option.name
                )

            if idx < len(self.options.options):
                if option.value is None:
                    option.value = option.default

                converter = self.command.converter(option.value)

                if option.modifier is OptionModifier.ConsumeRest:
                    # Consume the rest of the arguments in the command
                    option.value = " ".join(self.command.args[idx:])
                else:
                    try:
                        # Converts the value of an option according to the type.
                        converted = converter.convert(option.type)
                    except (ValueError, TypeError):
                        raise ConversionError(
                            f"Could not convert {option.value!r} into {option.type}",
                            option.name,
                        )

                    # set the value to the converted value if successfully converted,
                    # otherwise, set it to the old value
                    if converted is not None:
                        option.value = converted
                    else:
                        option.value = converter.value

            self.options.options[idx] = option


class ErrorContext(BaseContext):
    """A context to be passed to an error callback."""

    def __init__(self, command: Cmd, error: Exception, attrs: AttributeType = None):
        self.error = error
        super().__init__(command, attrs)


class BaseCallback:
    """The callback base class"""

    def __init__(self, func: Callable):
        self.func = func

    def __call__(self, *args, **kwargs):
        return self.func(*args, **kwargs)

    @property
    def is_coroutine(self):
        """Checks if callback is an async function."""
        return inspect.iscoroutinefunction(self.func)


class ErrorCallback(BaseCallback):
    """A callback for error handling."""

    def make_context(self, command: Cmd, error: Exception, attrs: AttributeType = None):
        """Create a new context based on a command object with the exception that was raised.

        Parameters
        ----------
        command : Cmd
            The command object.
        error : Exception
            The exception that gets raised.
        attrs : AttributeType
            Additional attributes to be passed to the callback context.

        Returns
        -------
        The context created with the exception.
        """
        return ErrorContext(command, error, attrs)


class Callback(BaseCallback):
    """A callback for handling command execution.

    Parameters
    ----------
    func : Callable
        A function to assign as callback.
    """

    def __init__(self, func: Callable):
        self.options = Options()
        self.errcall = None
        super().__init__(func)

    def make_context(self, command: Cmd, attrs: AttributeType = None) -> Context:
        """Create a new context based on a command object.

        Parameters
        ----------
        command : Cmd
            The command object.
        attrs : AttributeType
            Additional attributes to be passed to the callback context.

        Returns
        -------
        The context created.
        """
        options = self.options.copy()
        apply_params(command, options)

        return Context(command, options, attrs)

    def error(self, func: Callable) -> ErrorCallback:
        """Wraps a function and assigns it as an error callback.

        Parameters
        ----------
        func : Callable
            The function to wrap.

        Returns
        -------
        An ErrorCallback object.
        """
        self.errcall = ErrorCallback(func)
        return self.errcall


def callback_init(func: Callable) -> Callback:
    """Wraps a function as Callback.

    Parameters
    ----------
    func : Callable
        The function to wrap.

    Returns
    -------
    A Callback object.
    """
    return Callback(func)


def add_option(
    name: str,
    *,
    default: Any = None,
    modifier: OptionModifier = OptionModifier.NoModifier,
    type: BasicTypes = str,
):
    """A decorator for adding an option to a callback.

    This decorator also wraps the function as a callback if it's not a Callback.

    Parameters
    ----------
    name : str
        The option name.
    default : str
        Default value if argument is not specified.
    modifier : OptionModifier
        The option modifier
    type : BasicType
        Converts the value to the specified type.

    Raises
    ------
    TypeError
        If the target is not a function or a Callback.
    """

    def decorator(obj):
        if isinstance(obj, Callback):
            obj.options.add(name, default, modifier, type=type)
        elif isinstance(obj, Callable):
            obj = Callback(obj)
            obj.options.add(name, default, modifier, type=type)
        else:
            raise TypeError(f"Cannot add option to object {obj!r}")

        return obj

    return decorator
