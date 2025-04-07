import inspect
import typing
from typing import Any, Callable, Dict, List, Optional, Union

from cmdtools.base import Cmd, Executor
from cmdtools.callback import Attributes, Callback, ErrorCallback, AttributeType
from cmdtools.callback.option import OptionModifier
from cmdtools.converter.base import BasicTypes
from cmdtools.errors import CmdBaseException, NotFoundError

__all__ = ["Command", "Group"]


class BaseCommand:
    """The base class of command struct or class."""

    _callback: Optional[Callback]

    def __init__(self, name: str):
        self.name = name
        self._callback = None

    @property
    def callback(self) -> Callback:
        """Callback determined by function name."""
        if isinstance(self._callback, Callback):
            return self._callback
        else:
            cmdfun = getattr(self, self.name, None)
            errfun = getattr(self, "error_" + self.name, None)

            if inspect.ismethod(cmdfun):
                self._callback = Callback(cmdfun)

                if errfun:
                    self._callback.errcall = ErrorCallback(errfun)

                return self._callback
            else:
                raise CmdBaseException("Could not determine callback.")

    def add_option(
        self,
        name: str,
        *,
        default: Any = None,
        modifier: OptionModifier = OptionModifier.NoModifier,
        type: BasicTypes = str,
    ):
        """Adds an option to the callback.

        A wrapper for Options.add()

        Parameters
        ----------
        name : str
            The option name.
        default : Any
            The default value.
        modifier : OptionModifier
            The option modifier.
        append : bool
            Adds option with append mode.
        type : BasicType
            Converter target type.
        """
        self.callback.options.add(name, default, modifier, append=True, type=type)


class Command(BaseCommand):
    """A command struct or class.

    Parameters
    ----------
    name : str
        The name of the command.
    aliases : List[str]
        The aliases of the command.
    """

    def __init__(self, name: str, aliases: Optional[List[str]] = None):
        if aliases is None:
            self._aliases = []
        else:
            self._aliases = aliases
        super().__init__(name)

    @property
    def aliases(self) -> List[str]:
        """gets the command aliases if set."""
        if self._aliases:
            return self._aliases

        return getattr(self, "__aliases__", [])


class Container:
    """Container for command classes.

    Parameters
    ----------
    commands : List[Command]
        List of command structs or classes.
    """

    def __init__(self, commands: Optional[List[Command]] = None):
        if commands is None:
            self.commands = []
        else:
            self.commands = commands

    def __iter__(self):
        yield from self.commands

    def add_command(self, command: Command):
        self.commands.append(command)

    def get_names(self, get_aliases: bool = False) -> List[str]:
        """gets all command names stored in the container.

        Parameters
        ----------
        get_aliases : bool
            Include commands aliases.
        """
        names = [cmd.name for cmd in self.commands]

        if get_aliases:
            for aliases in [cmd.aliases for cmd in self.commands]:
                names.extend(aliases)

        return names

    def get_command(self, name: str) -> Optional[Command]:
        """gets a command object by name.

        Parameters
        ----------
        name : str
            Name of the command.
        """
        for cmd in self.commands:
            if cmd.name == name:
                return cmd

    def has_command(self, name: str) -> bool:
        """Checks if the container has the specified command.

        Parameters
        ----------
        name : str
            The command name.
        """
        return name in self.get_names()

    async def run(
        self, command: Cmd, *, attrs: AttributeType = None
    ):
        """Executes a matched command from the container.

        Parameters
        ----------
        command : Cmd
            The command to be executed.
        attrs : AttributeType
            Additional attributes to be passed to the callback context.

        Raises
        ------
        NotFoundError
            If the command is not found.
        """

        for cmd in self.commands:
            if cmd.name == command.name or command.name in cmd.aliases:
                executor = Executor(command, cmd.callback, attrs=attrs)

                if cmd.callback.is_coroutine:
                    return await executor.exec_coro()

                return executor.exec()

        raise NotFoundError(f"Command not found: {command.name}", command.name)


class GroupWrapper(Command):
    """A callback wrapper for functions.

    Parameters
    ----------
    name : str
        The command name.
    aliases : List[str]
        The command aliases.
    """

    def __init__(self, name: str, aliases: Optional[List[str]] = None):
        super().__init__(name, aliases)

    def __call__(self, *args, **kwargs):
        return self.callback(*args, **kwargs)

    @property
    def error_callback(self) -> Optional[ErrorCallback]:
        return self.callback.errcall


class Group(Container):
    """A group based container class.

    Parameters
    ----------
    name : str
        The group name
    commands : List[Command]
        List of command structs or classes.
    """

    def __init__(self, name: str, commands: Optional[List[Command]] = None):
        self.name = name
        super().__init__(commands)

    def command(self, name: str = "", *, aliases: Optional[List[str]] = None):
        """assigns the target command struct or class to the container.

        Parameters
        ----------
        name : str
            The name of the command
        aliases : List[str]
            The command aliases.
        """

        if aliases is None:
            aliases = []

        def decorator(obj):
            nonlocal name

            if inspect.isclass(obj) and Command in inspect.getmro(obj):
                if len(inspect.signature(obj.__init__).parameters) > 1:
                    _obj = obj(name)
                else:
                    _obj = obj()

                    if name:
                        _obj.name = name

                if aliases:
                    _obj._aliases = aliases

                self.commands.append(_obj)
                obj = _obj
            else:
                if not name:
                    if isinstance(obj, Callback):
                        name = obj.func.__name__
                    elif isinstance(obj, Callable):
                        name = obj.__name__

                wrapper = GroupWrapper(name, aliases)
                if isinstance(obj, Callback):
                    wrapper._callback = obj
                else:
                    wrapper._callback = Callback(obj)
                self.commands.append(wrapper)

                return wrapper
            return obj

        return decorator

    def add_option(
        self,
        name: str,
        *,
        default: Any = None,
        modifier: OptionModifier = OptionModifier.NoModifier,
        type: BasicTypes = str,
    ):
        """Adds an option to callback.

        Parameters
        ----------
        name : str
            The option name.
        default : str
            Default value if argument is not specified.
        modifier : OptionModifier
            The option modifier,
            some modifier used to modify the value.
        type : BasicType
            Convert the value to specified type.

        Raises
        ------
        TypeError
            When adding option to non Command instance.
        """

        def decorator(obj):
            if isinstance(obj, Command):
                obj.callback.options.add(name, default, modifier, type=type)
            else:
                raise TypeError("Cannot add option to non Command instance.")
            return obj

        return decorator
