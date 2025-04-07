from __future__ import annotations

from typing import Any, Dict, List, Optional, Union, Type

from cmdtools import utils
from cmdtools.callback import Attributes, Callback, AttributeType, Option
from cmdtools.converter.converter import Converter

__all__ = ["Cmd", "Executor", "execute"]


class Cmd:
    """A base class for creating a command object.

    Parameters
    ----------
    text : str
        Command text to be parsed, for example: '/ping 8.8.8.8'
    prefix : str
        The prefix of the command
    converter : :class:`Converter`
        Converter for arguments.

    Examples
    --------
    Creating a basic command object::

        from cmdtools import Cmd

        x = Cmd("/test")

        if x.name == "test":
            print("test ok!")


    """

    def __init__(
        self, text: str, prefix: str = "/", *, converter: Type[Converter] = Converter
    ):
        self.text = text
        self.prefix = utils.PrefixChecker(text, prefix)
        self.converter = converter

    @property
    def _args(self) -> List[str]:
        if self.prefix.strip_prefix is not None:
            return utils.splitargs(self.prefix.strip_prefix)

        return []

    @property
    def args(self) -> List[str]:
        """List of the command's arguments"""
        if len(self._args) > 1:
            return self._args[1:]

        return []

    @property
    def name(self) -> str:
        """The name of the command if valid, otherwise return empty string"""
        if len(self._args) >= 1:
            return self._args[0]

        return ""


class Executor:
    """A class for creating custom command executor

    Parameters
    ----------
    command : :class:`Cmd`
        The command object to be executed.
    callback : :class:`Callback`
        A function that will be invoked when the command is executed.
    attrs
        Additional attributes to be passed to the callback context.

    Examples
    --------
    Executing a command with a custom executor::

        from cmdtools import Cmd, Executor
        from cmdtools.callback import callback_init

        cmd = Cmd("/somecmd")

        @callback_init
        def some_callback(ctx):
            print("Wicked insane!")

        x = Executor(cmd, some_callback)
        x.exec()


    Raises
    ------
    TypeError
        - If callback is not a Callback.
        - If callback types do not match.
    """

    def __init__(
        self,
        command: Cmd,
        callback: Callback,
        *,
        attrs: AttributeType = None,
    ):
        self.command = command
        if not isinstance(attrs, Attributes):
            if isinstance(attrs, dict):
                self.attrs = Attributes(attrs)
            else:
                self.attrs = Attributes()
        else:
            self.attrs = attrs

        if not isinstance(callback, Callback):
            raise TypeError(f"{callback!r} is not a Callback.")
        self.callback = callback

        if self.callback.errcall:
            if self.callback.is_coroutine != self.callback.errcall.is_coroutine:
                raise TypeError("Both callback types must be either async or regular functions.")

    def exec(self) -> Optional[Any]:
        """Executes the given command

        Returns
        -------
        Anything retured in the callback.

        Raises
        ------
        Exception
            Any exception raised during execution
            if error callback is not set.
        """
        result = None

        try:
            context = self.callback.make_context(self.command, self.attrs)
            result = self.callback(context)
        except Exception as exception:
            if self.callback.errcall:
                error_context = self.callback.errcall.make_context(
                    self.command, exception, self.attrs
                )
                result = self.callback.errcall(error_context)
            else:
                raise exception

        return result

    async def exec_coro(self) -> Optional[Any]:
        """Executes the given command for async callbacks

        Returns
        -------
        The return value from the callback if the command executed successfully,
        or the return value from the error callback if an exception occurred and an error callback is set.

        Raises
        ------
        Exception
            Any exception raised during execution
            if error callback is not set.
        """
        result = None

        try:
            context = self.callback.make_context(self.command, self.attrs)
            result = await self.callback(context)
        except Exception as exception:
            if self.callback.errcall:
                error_context = self.callback.errcall.make_context(
                    self.command, exception, self.attrs
                )
                result = await self.callback.errcall(error_context)
            else:
                raise exception

        return result


async def execute(
    command: Cmd,
    callback: Callback,
    *,
    attrs: AttributeType = None,
):
    """A simple executor using :class:`Executor`

    Parameters
    ----------
    command : Cmd
        The command object to be executed.
    callback : Callback
        A function that will be invoked when the command is executed.
    attrs : AttributeType
        Additional attributes to be passed to the callback context.

    Returns
    -------
    The return value from the callback if the command executed successfully,
    or the return value from the error callback if an exception occurred and an error callback is set.

    Raises
    ------
    Exception
        Any exception raised during execution if no error callback is assigned.
    TypeError
        - If callback is not a :class:`Callback`.
        - If callback types do not match.
    """
    executor = Executor(command, callback, attrs=attrs)

    if callback.is_coroutine:
        return await executor.exec_coro()

    return executor.exec()
