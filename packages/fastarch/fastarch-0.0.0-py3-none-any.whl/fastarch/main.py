from fastarch.management.manager import CommandManager


def main(*args, **kwargs):
    manager = CommandManager()
    manager.run_command()
