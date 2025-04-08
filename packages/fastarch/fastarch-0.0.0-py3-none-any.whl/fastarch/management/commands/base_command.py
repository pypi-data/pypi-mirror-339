from typing import Any


class Argument:
    def __init__(
        self,
        name: str,
        positional: bool = True,
        type: type | None = None,
        required: bool = False,
        choice: list[Any] = None,
        help: str = "",
        short_name: str | None = None,
        action: str | None = None,
    ) -> None:
        self.name = name
        self.positional = positional
        self.choice = choice or []
        self.required = required
        self.type = type
        self.help = help
        self.short_name = short_name
        self.action = action

    def to_dict(self) -> dict[str, Any]:
        param_dict = {}
        if self.positional:
            param_dict["name_or_flags"] = [self.name]
        else:
            param_dict["required"] = self.required
            if self.action:
                param_dict["action"] = self.action
            if self.short_name:
                param_dict["name_or_flags"] = [f"-{self.short_name}", f"--{self.name}"]
            else:
                param_dict["name_or_flags"] = [f"--{self.name}"]

        if self.choice and not self.action:
            param_dict["choice"] = self.choice
        if self.type and not self.action:
            param_dict["type"] = self.type
        if self.help:
            param_dict["help"] = self.help

        return param_dict


class BaseCommand:
    name = "base"
    help = "It is a base command"
    arguments = []

    def __init__(self, args):
        self.args = args

    @classmethod
    def add_command_arguments(cls, parser):
        for argument in cls.arguments:
            params = argument.to_dict()
            command = params.pop("name_or_flags")
            parser.add_argument(*command, **params)

    def execute(self):
        print(f"Выполняется команда {self.name} с аргументами: {self.args}")
