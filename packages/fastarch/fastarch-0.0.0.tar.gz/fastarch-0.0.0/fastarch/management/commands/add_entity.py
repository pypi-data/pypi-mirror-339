from .base_command import Argument, BaseCommand


class AddEntityCommand(BaseCommand):
    name = "add_entity"
    help = "Create new entity on all levels to your project"
    arguments = [
        Argument("name", type=str),
        Argument(
            "skip",
            short_name="s",
            positional=False,
            action="store_false",
            required=True,
        ),
    ]
