from cmdtools.errors import CmdBaseException

__all__ = ["ParameterParsingError", "parse_params", "apply_params"]


class ParameterParsingError(CmdBaseException):
    def __init__(self, message: str, name: str = ""):
        self.message = message
        self.name = name
        super().__init__(message)


def parse_params(args):
    """Parse command arguments into parameters and positional arguments.

    Parameters
    ----------
    args : list
        List of command arguments.

    Returns
    -------
    A tuple containing parameters and positional arguments.
    """
    result = []
    positional = []
    params = []

    for arg in args:
        param = arg.split('=', 1)

        if len(param) > 1:
            if param[0] not in params:
                result.append(param)
                params.append(param[0])
            else:
                raise ParameterParsingError("Duplicate parameter: " + param[0], param[0])
        else:
            positional.append(param[0])

    return result, positional


def apply_params(command, options):
    """Apply parsed parameters to command options.

    Parameters
    ----------
    command : Command
        Source of command arguments.
    options : dict
        The target command options.
    """
    opts_applied = []
    param_args, positional_args = parse_params(command.args)

    for param in param_args:
        option = options.get(param[0])

        if option:
            option.value = param[1]
            opts_applied.append(param[0])

    for arg in positional_args:
        for option in options:
            if option.name not in opts_applied:
                option.value = arg
                opts_applied.append(option.name)
                break
