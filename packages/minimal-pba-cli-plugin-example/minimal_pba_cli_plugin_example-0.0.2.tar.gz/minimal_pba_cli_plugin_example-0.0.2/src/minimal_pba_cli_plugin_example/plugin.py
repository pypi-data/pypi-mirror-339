from typing import Annotated

import typer


greet = typer.Typer()


@greet.command()
def morning(name: Annotated[str, typer.Argument()] = "world"):
    """Say good morning to NAME."""

    typer.echo(f"Good morning {name}!")


@greet.command()
def evening(name: Annotated[str, typer.Argument()] = "world"):
    """Say good evening to NAME."""

    typer.echo(f"Good evening {name}!")


def salute(name: Annotated[str, typer.Argument()] = "world"):
    """Say salutations to NAME."""

    typer.echo(f"Salutations {name}!")


groups = {
    "greet": greet,
}

commands = {
    "salute": salute,
}
