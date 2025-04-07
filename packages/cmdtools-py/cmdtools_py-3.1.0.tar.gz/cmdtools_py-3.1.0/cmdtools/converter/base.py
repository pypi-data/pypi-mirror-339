from typing import Type, Union

try:
    from typing import TypeAlias
except ImportError:
    from typing_extensions import TypeAlias

__all__ = [
    "BaseConverter",
    "BaseType",
    "BasicTypes",
]

BaseType: TypeAlias = Union[int, float, str, bool]
BasicTypes: TypeAlias = Type[BaseType]


class BaseConverter:
    """The converter base class"""

    def __init__(self, value: BaseType):
        self.value = value
