"""Console script for shoestring_assembler."""

import shoestring_assembler
from shoestring_assembler.assembler import Assembler
from shoestring_assembler.models.recipe import Recipe
from shoestring_assembler.user_config import UserConfig
from shoestring_assembler.display import Display
from shoestring_assembler.filesystem import SolutionFilesystem
from shoestring_assembler.git import SolutionGitVC, GetSolutionUsingGit
from shoestring_assembler.docker import Docker

import typer
from typing_extensions import Annotated
import os
import sys

typer_app = typer.Typer(name="Shoestring Assembler", no_args_is_help=True)


@typer_app.command()
def check_recipe(
    recipe_location: Annotated[
        str, typer.Argument(help="Path to recipe file")
    ] = "./recipe.toml",
):
    Display.print_top_header("Checking Recipe")
    Recipe.load(recipe_location)
    Display.print_top_header("Finished")


@typer_app.command()
def download(
    verbose: Annotated[
        bool, typer.Option("--verbose", help="Show extra logs.")
    ] = False,
):
    """
    Downloads the specified solution
    """
    execute(Commands.DOWNLOAD,verbose=verbose)


@typer_app.command()
def update(
    version: Annotated[
        str, typer.Argument(help="Update to this version. (optional)")
    ] = "",
    verbose: Annotated[
        bool, typer.Option("--verbose", help="Show extra logs.")
    ] = False,
    yes: Annotated[
        bool,
        typer.Option(
            "--yes", "-y", help="Automatically download and assemble the latest version"
        ),
    ] = False,
    recipe_location: Annotated[
        str, typer.Argument(help="Path to recipe file")
    ] = "./recipe.toml",
):
    """
    Updates the solution to the specified version. If a version is not specified - it lists the available versions that you can choose from.
    """
    execute(Commands.UPDATE,recipe_location=recipe_location,verbose=verbose)


@typer_app.command()
def assemble(
    recipe_location: Annotated[
        str, typer.Argument(help="Path to recipe file")
    ] = "./recipe.toml",
    download: bool = True,
    verbose: Annotated[
        bool, typer.Option("--verbose", help="Show extra logs.")
    ] = False,
):
    """
    Assembles the solution using the provided recipe
    """
    execute(Commands.ASSEMBLE, recipe_location=recipe_location, verbose=verbose)


@typer_app.command()
def reconfigure(
    recipe_location: Annotated[
        str, typer.Argument(help="Path to recipe file")
    ] = "./recipe.toml",
    verbose: Annotated[
        bool, typer.Option("--verbose", help="Show extra logs.")
    ] = False,
):
    execute(Commands.RECONFIGURE, recipe_location=recipe_location, verbose=verbose)


@typer_app.command()
def build():
    execute(Commands.BUILD)


@typer_app.command()
def setup():
    execute(Commands.SETUP)


@typer_app.command()
def start():
    execute(Commands.START)


@typer_app.callback(invoke_without_command=True)
def main(
    version: Annotated[
        bool, typer.Option("--version", "-v", help="Assembler version")
    ] = False,
):
    if version:
        Display.print_log(
            f"Shoestring Assembler version {shoestring_assembler.__version__}"
        )
    else:
        pass  # TODO display menu


from enum import Enum, unique
from .engine.engine import Engine
from .views.plain_cli import PlainCLI

@unique
class Commands(Enum):
    DOWNLOAD = "download"
    UPDATE = "update"
    ASSEMBLE = "assemble"
    RECONFIGURE = "reconfigure"
    BUILD = "build"
    SETUP = "setup"
    START = "start"

def execute(command,*,recipe_location=None,verbose=False):
    if verbose:
        Display.log_level = 5

    ui = PlainCLI()
    engine = Engine(update_callback=ui.notify_fn)
    
    match(command):
        case Commands.DOWNLOAD:
            engine.init_download()
        case Commands.UPDATE:
            engine.init_update()
        case Commands.ASSEMBLE:
            engine.init_assemble()
        case Commands.RECONFIGURE:
            engine.init_reconfigure()
        case Commands.BUILD:
            engine.init_build()
        case Commands.SETUP:
            engine.init_setup()
        case Commands.START:
            engine.init_start()
        case _:
            Display.print_error("Unknown Command")
            sys.exit(255)
    
    ui.execute(engine)

def app():
    try:
        if os.geteuid() == 0:
            Display.print_error(
                "To try prevent you from accidentally breaking things, this program won't run with sudo or as root! \nRun it again without sudo or change to a non-root user."
            )
            sys.exit(255)
        typer_app()
    finally:
        Display.finalise_log()


if __name__ == "__main__":
    app()
"""
* shoestring
    * bootstrap (maybe for a separate developer focussed tool?)
"""
