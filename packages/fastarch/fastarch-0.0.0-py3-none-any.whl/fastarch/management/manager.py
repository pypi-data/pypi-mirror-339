import argparse

import fastarch.management.commands as commands


class CommandManager:
    def __init__(self):
        self.commands = commands.mapping
        self.parser = self.create_parser()

    def create_parser(self):
        parser = argparse.ArgumentParser(
            description="""
            FastArch is a simple framework based on FastAPI.\n
            You can quickly create project follow Clean Architecture idea.
            """,
            formatter_class=argparse.RawTextHelpFormatter,
        )
        subparsers = parser.add_subparsers(
            dest="command",
            help="Choice the command:",
            required=True,
        )

        for command_name, command_class in self.commands.items():
            command_parser = subparsers.add_parser(
                command_name, help=command_class.help
            )
            command_parser.set_defaults(command=command_name)
            command_class.add_command_arguments(command_parser)

        return parser

    def run_command(self):
        parsed_args = self.parser.parse_args()
        command_name = parsed_args.command
        command_class = self.commands[command_name]
        command_instance = command_class(parsed_args)
        command_instance.execute()
