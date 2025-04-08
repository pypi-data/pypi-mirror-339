from .base_command import Argument, BaseCommand


class CreateProjectCommand(BaseCommand):
    name = "create_project"
    help = "Create new project with base entities"
    arguments = [
        Argument("name", type=str),
        Argument("skip", short_name="s", positional=False, action="store_false"),
    ]
