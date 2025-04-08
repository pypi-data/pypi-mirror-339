import sys
import os
from pathlib import Path
from shoestring_assembler.models import SolutionModel


try:
    from pathlib import UnsupportedOperation
except ImportError:
    UnsupportedOperation = NotImplementedError


from .constants import Contants
from .display import Display


class SolutionFilesystem:
    @classmethod
    def clean(cls, clean_sources=True):
        Display.print_header("Cleaning")
        # TODO
        if clean_sources:
            rmtree(Path(Contants.MODULE_SOURCE_FILES_DIR))
        Display.print_complete("Old files cleared")

    @classmethod
    def verify(cls, solution_model: SolutionModel, check_sources=False):
        Display.print_header("Verifying filesystem structure")

        all_ok = True

        # check solution directories
        all_ok = check_dir(Contants.SOLUTION_FILES_DIR) and all_ok
        all_ok = check_dir(Contants.SOLUTION_CONFIG_DIR) and all_ok
        for source in solution_model.sources:
            all_ok = (
                check_or_create_dir(f"{Contants.SOLUTION_CONFIG_DIR}/{source.name}")
                and all_ok
            )

        all_ok = check_or_create_dir(Contants.MODULE_SOURCE_FILES_DIR) and all_ok
        if check_sources:
            for source in solution_model.sources:
                all_ok = (
                    check_dir(f"{Contants.MODULE_SOURCE_FILES_DIR}/{source.name}")
                    and all_ok
                )

        # check data directories
        all_ok = check_or_create_dir(Contants.DATA_DIR) and all_ok
        for instance in solution_model.module_iterator():
            all_ok = check_or_create_dir(f"data/{instance.name}") and all_ok

        # check user config directories
        all_ok = check_or_create_dir(Contants.USER_CONFIG_DIR) and all_ok
        for instance in solution_model.module_iterator():
            all_ok = (
                check_or_create_dir(f"{Contants.USER_CONFIG_DIR}/{instance.name}") and all_ok
            )

        # check log directories
        all_ok = check_or_create_dir("logs") and all_ok
        # for source_name in self.recipe.sources.keys():
        #     all_ok = check_or_create_dir(f"logs/{source_name}") and all_ok

        if not all_ok:
            Display.print_error(
                "Filesystem structure failed validation - unable to continue"
            )
            sys.exit(255)
        else:
            Display.print_complete("Filesystem structure valid")


class FilesystemSource:

    @staticmethod
    def fetch(name, details, console=None):
        mode = details.get("mode", "copy")
        path = details["path"]  # could throw error but shouldn't due to validation

        Display.print_log(f"type: file, mode: {mode}", console=console)

        src_path = Path.resolve(Path(path))
        dest_path = Path.resolve(Path.cwd()) / Contants.MODULE_SOURCE_FILES_DIR / name

        if mode == "copy":
            do_copy(src_path, dest_path)
            Display.print_log(
                f"{src_path} [green]copied[/green] to {dest_path}", console=console
            )
        elif mode == "link":
            try:
                dest_path.symlink_to(src_path, target_is_directory=True)
                Display.print_log(
                    f"{src_path} [green]linked[/green] to {dest_path}", console=console
                )
            except UnsupportedOperation:
                Display.print_error(
                    f"Operating system does not support symlinks. Could not link [purple]{src_path}[/purple] to [purple]{dest_path}[/purple] for source {name}. Consider changing [cyan]mode[/cyan] to [cyan]copy[/cyan].",
                    console=console,
                )
                return False
            except FileExistsError:
                Display.print_error(
                    f"Files already present at destination - Could not link [purple]{src_path}[/purple] to [purple]{dest_path}[/purple] for source {name}.",
                    console=console,
                )
                return False

        return True

# Utility function implementations


def check_dir(rel_path):
    full_path = Path.resolve(Path.cwd()) / Path(rel_path)
    if full_path.is_dir():
        Display.print_log(f"[green]\[ok] [white] {rel_path}")
        return True
    else:
        Display.print_log(f"[red]\[error - not found] {rel_path}")
        return False


def check_or_create_dir(rel_path):
    full_path = Path.resolve(Path.cwd()) / Path(rel_path)
    try:
        full_path.mkdir(exist_ok=False)
        Display.print_log(f"[green]\[created] [white]{rel_path}")
    except FileExistsError:
        try:
            full_path.mkdir(exist_ok=True)
            Display.print_log(f"[green]\[ok] [white] {rel_path}")
        except FileExistsError:
            Display.print_log(f"[red]\[error - can't create] {rel_path}")
            return False
    except FileNotFoundError:
        Display.print_log(f"[red]\[error - no parent] {rel_path}")
        return False

    return True


if sys.version_info[0] == 3 and sys.version_info[1] < 12:

    def rmtree(root: Path):
        Display.print_log(f"Clearing {root}")
        for walk_root, dirs, files in os.walk(root, topdown=False):
            walk_root = Path(walk_root)
            for name in files:
                (walk_root / name).unlink()
            for name in dirs:
                path = walk_root / name
                if path.is_symlink():
                    path.unlink()
                else:
                    path.rmdir()

else:

    def rmtree(root: Path):
        Display.print_log(f"Clearing {root}")
        for root, dirs, files in root.walk(top_down=False):
            for name in files:
                (root / name).unlink()
            for name in dirs:
                (root / name).rmdir()


if sys.version_info[0] == 3 and sys.version_info[1] < 14:

    def do_copy(src_path, dest_path, create_dirs=False):
        import shutil

        shutil.copytree(src_path, dest_path, dirs_exist_ok=create_dirs)

else:

    def do_copy(src_path, dest_path, create_dirs=False):
        src_path.copy_into(dest_path)
