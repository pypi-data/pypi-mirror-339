from fastarch.management.commands.add_entity import AddEntityCommand
from fastarch.management.commands.create_project import CreateProjectCommand

mapping = {
    "add_entity": AddEntityCommand,
    "create_project": CreateProjectCommand,
}

__all__ = ["mapping"]
