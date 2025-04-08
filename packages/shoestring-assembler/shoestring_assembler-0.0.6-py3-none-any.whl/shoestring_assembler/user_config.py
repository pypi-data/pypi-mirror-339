import jinja2
from pathlib import Path
import sys
import os
import re

from .display import Display
from .constants import Contants

from shoestring_assembler.models import SolutionModel, ServiceModuleModel

version_regex = re.compile("^\s*(\d+)\.(\d+)\s*$")


class UserConfig:
    @staticmethod
    def configure(solution_model: SolutionModel):
        Display.print_header("Configuring User Config")
        for service_module in solution_model.service_modules:
            if service_module.user_config.requires_configuration:
                UserConfig.apply_template(service_module)

        Display.print_complete(f"User config ready")

    @staticmethod
    def apply_template(sm: ServiceModuleModel):
        # setup for template engine
        jinja2_env = jinja2.Environment(
            loader=jinja2.FileSystemLoader(sm.user_config.template.abs_path)
        )

        rel_dir_list, rel_file_list = walk_dir(sm.user_config.template.abs_path)

        for dir_rel_path in rel_dir_list:  # make directories as needed
            (sm.user_config.abs_path / dir_rel_path).mkdir(exist_ok=True)

        for file_rel_path in rel_file_list:  # render each template file
            templ = jinja2_env.get_template(str(file_rel_path))
            dest_file = sm.user_config.abs_path / file_rel_path
            with dest_file.open("w") as f:
                for segment in templ.generate(sm.user_config.context):
                    f.write(segment)

        # write version file
        sm.user_config.version = sm.user_config.template.version

        # write answers
        sm.user_config.prev_answers = sm.user_config.answers


if sys.version_info[0] == 3 and sys.version_info[1] < 12:

    def walk_dir(root: Path):

        dir_set = []
        file_set = []

        for raw_base, dirs, files in os.walk(root, topdown=True):
            base = Path(raw_base)

            if base == root / Contants.TEMPLATE_MANAGEMENT_SUBDIR:
                continue  # ignore all files in template management directory

            rel_base = Path(raw_base).relative_to(root)
            for name in files:
                file_set.append(rel_base / name)
            for name in dirs:
                if (base / name).is_symlink():
                    # this isn't expected to happen but accounting for it just in case
                    file_set.append(rel_base / name)
                else:
                    dir_set.append(rel_base / name)

        return dir_set, file_set

else:

    def walk_dir(root: Path):
        dir_set = []
        file_set = []

        for base, dirs, files in root.walk(top_down=True):
            if base == root / Contants.TEMPLATE_MANAGEMENT_SUBDIR:
                continue  # ignore all files in template management directory
            rel_base = base.relative_to(root)
            for name in files:
                file_set.append(rel_base / name)
            for name in dirs:
                dir_set.append(rel_base / name)

        return dir_set, file_set


"""
Consider in Future:
* Looping prompts - e.g. power factor entry in PM analysis
* Cross service module references - e.g. fetch all specified machine names and loop over them
"""
