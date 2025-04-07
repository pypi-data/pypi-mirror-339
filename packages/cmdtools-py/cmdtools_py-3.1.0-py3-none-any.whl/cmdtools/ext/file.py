from __future__ import annotations

import importlib
import importlib.util
import inspect
import os
from typing import Callable

from cmdtools.callback import Callback, ErrorCallback
from cmdtools.ext.command import Command, Container, GroupWrapper
from cmdtools.errors import CmdBaseException

__all__ = ["ModuleLoader"]


class ModuleLoader(Container):
    """A command module loader class.

    Parameters
    ----------
    fpath : str
        Path to the module.
    load_classes : bool
        Loads defined class type commands if true,
        otherwise loads the module as a :class:`Command`.

    Raises
    ------
    CmdBaseException
        - If failed to load module.
        - If the module failed to initialized.
        - If the callback loaded is not a function type.
    TypeError
        If aliases is not a list, when loading module as command file
    """

    def __init__(self, fpath: str, *, load_classes: bool = True):
        self.path = fpath
        super().__init__()

        # load module directly from source file with the exec_module() method
        spec = importlib.util.spec_from_file_location(
            fpath.rsplit(os.sep, 1)[-1].rstrip(".py"), fpath
        )

        if spec:
            module = importlib.util.module_from_spec(spec)

            if spec.loader:
                spec.loader.exec_module(module)
            else:
                raise CmdBaseException("Cannot initialize module, could not get module loader: " + fpath)
        else:
            raise CmdBaseException("Could not load module: " + fpath)

        if load_classes:
            for _, obj in module.__dict__.items():
                if inspect.isclass(obj) and obj.__module__ == spec.name:
                    if Command in inspect.getmro(obj):
                        self.commands.append(obj())
        else:
            aliases = getattr(module, "__aliases__", None)
            callback = getattr(module, spec.name, None)
            error_callback = getattr(module, "error_" + spec.name, None)

            if not aliases:
                aliases = []

            if not isinstance(aliases, list):
                raise TypeError("aliases is not list str type.")
            if not isinstance(callback, Callable):
                raise CmdBaseException("Could not load callback.")

            wrapper = GroupWrapper(spec.name, aliases)
            if not isinstance(callback, Callback):
                wrapper._callback = Callback(callback)

            else:
                wrapper._callback = callback

            # An edge case where there is no way to assign error callback for the callback function
            if isinstance(error_callback, Callable) \
                and not isinstance(error_callback, Callback) \
                and wrapper.callback.errcall is None:
                wrapper.callback.errcall = ErrorCallback(error_callback)

            self.commands.append(wrapper)
