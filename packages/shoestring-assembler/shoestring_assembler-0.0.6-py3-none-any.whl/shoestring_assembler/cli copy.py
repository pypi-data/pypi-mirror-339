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

from rich.prompt import Prompt, Confirm

typer_app = typer.Typer(name="Shoestring Assembler", no_args_is_help=True)


CANCEL_PHRASE = "cancel"


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
    if verbose:
        Display.log_level = 5

    Display.print_top_header("Updating Solution")

    solution_version_control = SolutionGitVC()

    if not version:
        if not solution_version_control.is_update_available():
            Display.print_notification("Latest version installed.")
            return
        else:
            Display.print_notification("A new version is available.")
            available_versions = solution_version_control.list_updates()
            if yes:
                version = available_versions[0]
            elif Confirm.ask("? Do you want to update now?", default=True):
                selected_version = Prompt.ask(
                    "? Select a version?",
                    choices=available_versions
                    + [
                        CANCEL_PHRASE,
                    ],
                    default=available_versions[0],
                )
                if selected_version != CANCEL_PHRASE:
                    version = selected_version

    if version:
        updated = solution_version_control.do_update(version)
        if updated:
            if yes or Confirm.ask(
                "? Do you want to assemble the solution now?", default=True
            ):
                try:
                    assemble(recipe_location)
                    return
                except SystemExit:
                    Display.print_error(
                        "Solution assembly failed. If you want to run it again use: [green]shoestring assemble[/green]"
                    )
                    raise
    else:
        Display.print_log(
            "If you want to update later - run: [green]shoestring update <version>[/green]"
        )

    Display.print_top_header("Finished")


@typer_app.command()
def check_recipe(
    recipe_location: Annotated[
        str, typer.Argument(help="Path to recipe file")
    ] = "./recipe.toml",
):
    Display.print_top_header("Checking Recipe")
    Recipe.load(recipe_location)
    Display.print_top_header("Finished")


@typer_app.command(name="test")
def bootstrap(
    recipe: Annotated[
        str, typer.Argument(help="Path to recipe file")
    ] = "./recipe.toml",
    verbose: Annotated[
        bool, typer.Option("--verbose", help="Show extra logs.")
    ] = False,
):
    """
    Uses templates to bootstrap the solution config for the specified sources
    """
    if verbose:
        Display.log_level = 5
    from .engine.engine import Engine
    from .views.plain_cli import PlainCLI

    ui = PlainCLI()
    engine = Engine(update_callback=ui.notify_fn)
    engine.init_download()
    ui.execute(engine)
    # action = engine.start_process(engine.update_solution(False, None))
    # event = ui.handle(action)
    # while event is not None:
    #     action = engine.send_event(event)
    #     event = ui.handle(action)


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
    if verbose:
        Display.log_level = 5
    Display.print_top_header("Assembling Solution")

    recipe = Recipe.load(recipe_location)
    SolutionFilesystem.clean(clean_sources=download)
    SolutionFilesystem.verify(recipe, check_sources=not download)
    Assembler(recipe).load_sources(do_gather=download)
    Assembler(recipe).generate_compose_file()
    UserConfig.configure(recipe)
    Display.print_top_header("Finished")
    Display.print_next_steps(
        "* Configure the service modules according to your needs (refer to the guide for details) \n\n* Once the solution is ready - run [white]shoestring build[/white] to build the solution"
    )


import urllib
import yaml
from rich.prompt import Prompt
import subprocess
from .solution_picker import SolutionPickerApp


# Temporary implementation - refactor once proof-of-concept complete
@typer_app.command()
def get(
    verbose: Annotated[
        bool, typer.Option("--verbose", help="Show extra logs.")
    ] = False,
):
    """
    Downloads the specified solution
    """
    if verbose:
        Display.log_level = 5

    Display.print_top_header("Get Solution")

    Display.print_header(f"Selecting Solution")
    # fetch solution list
    list_branch = os.getenv("SHOESTRING_LIST_BRANCH", "main")
    try:
        with urllib.request.urlopen(
            f"https://github.com/DigitalShoestringSolutions/solution_list/raw/refs/heads/{list_branch}/list.yaml"
        ) as web_in:
            content = web_in.read()
            provider_list = yaml.safe_load(content)
    except urllib.error.URLError:
        Display.print_error("Unable to fetch latest solution list")
        return

    selected = SolutionPickerApp(provider_list).run()

    if selected == None:
        Display.print_log("Solution selection cancelled")
    else:
        Display.print_log(f"Selected [green]{selected['name']}[/green]")

        if GetSolutionUsingGit.download(selected):
            Display.print_complete("Done")
            Display.print_next_steps(
                "* Move to the solution folder using [white]cd[/white]\n\n"
                + "* Once in the folder assemble the solution using [white]shoestring assemble[/white]"
            )
        else:
            Display.print_error("Unable to download solution")
    Display.print_top_header("Finished")


@typer_app.command()
def build():
    Display.print_top_header("Starting solution")
    built = Docker.build()
    if built:
        Display.print_complete("Solution Built")
        Display.print_next_steps(
            "To run the solution use [white]shoestring start[/white]"
        )
    else:
        Display.print_error("Solution Building Failed")
    Display.print_top_header("Finished")


@typer_app.command()
def setup():
    Display.print_top_header("Setting up Service Modules")

    Docker.setup_containers()

    Display.print_top_header("Finished")


@typer_app.command()
def start():
    Display.print_top_header("Starting solution")
    started = Docker.start()
    if started:
        Display.print_complete("Solution is now running in the background")
    Display.print_top_header("Finished")


@typer_app.command()
def reconfigure(
    recipe_location: Annotated[
        str, typer.Argument(help="Path to recipe file")
    ] = "./recipe.toml",
    verbose: Annotated[
        bool, typer.Option("--verbose", help="Show extra logs.")
    ] = False,
):
    if verbose:
        Display.log_level = 5
    Display.print_top_header("Reconfiguring user config")
    recipe = Recipe.load(recipe_location)
    UserConfig.reconfigure(recipe)
    Display.print_top_header("Finished")


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
