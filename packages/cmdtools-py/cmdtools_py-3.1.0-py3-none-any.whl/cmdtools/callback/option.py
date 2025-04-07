import dataclasses
import enum
from typing import Any, List, Optional
from cmdtools.converter.base import BaseType, BasicTypes

__all__ = [
    "OptionModifier",
    "Option",
    "Options"
]


class OptionModifier(enum.Enum):
    """An option modifier.

    NoModifier
        Does not modify the value.
    ConsumeRest
        Consume the rest of the arguments in the command
    """

    NoModifier = "no_modifier"
    ConsumeRest = "consume_rest"


@dataclasses.dataclass
class Option:
    """An option dataclass.

    Parameters
    ----------
    name : str
        The name of the option.
    value : BaseType
        The value of the option.
    default : BaseType
        The default value of the option.
    modifier : OptionModifier
        The option modifier,
        some modifier used to modify the value.
    type : BasicType
        Converter target type.
    """

    name: str
    value: Optional[BaseType] = None
    default: Optional[BaseType] = None
    modifier: OptionModifier = OptionModifier.NoModifier
    type: BasicTypes = str


class Options:
    """An option container class.

    Parameters
    ----------
    options : List[Option]
        List of options.
    """

    def __init__(self, options: Optional[List[Option]] = None):
        if options is None:
            options = []
        self.options = options

    def __iter__(self):
        yield from self.options

    def __getattr__(self, name: str) -> Optional[BaseType]:
        option = self.get(name)

        if option:
            return option.value

    def copy(self):
        """Creates a new Options instance with copies of all stored options."""
        options = []

        for option in self.options:
            opt = Option(
                name=option.name,
                value=option.value,
                default=option.default,
                modifier=option.modifier,
                type=option.type
            )
            options.append(opt)
        return Options(options)

    def get(self, name: str) -> Optional[Option]:
        """Gets an option by name.

        Parameters
        ----------
        name : str
            The name of the option.
        """
        for option in self.options:
            if option.name == name:
                return option

    def has_option(self, name: str) -> Optional[int]:
        """Checks if the container has an option.

        Parameters
        ----------
        name : str
            The name of the option.
        """
        if self.get(name):
            return True

        return False

    def add(
        self,
        name: str,
        default: Any = None,
        modifier: OptionModifier = OptionModifier.NoModifier,
        append: bool = False,
        type: BasicTypes = str,
    ):
        """Adds an option to the container.

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
        option = self.has_option(name)

        if not option:
            option = Option(
                name=name,
                value=None,
                default=default,
                modifier=modifier,
                type=type
            )

            if not append:
                self.options.insert(0, option)
            else:
                self.options.append(option)
