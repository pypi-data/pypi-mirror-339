from .recipe import Recipe
from shoestring_assembler.models.service_module import ServiceModuleModel
from shoestring_assembler.models.infrastructure_module import InfrastructureModule
from shoestring_assembler.models.source import SourceModel
from shoestring_assembler.git import SolutionGitVC
from shoestring_assembler.views.interface.updates import FatalError
from pathlib import Path
from .common import ModelMap
from itertools import chain
import yaml

"""
ShoestringCommunityModel
provider_list
selected solution
available solution versions
selected version

available updates
selected version
"""


class SolutionModel:
    def __init__(self):
        working_dir = Path.resolve(Path.cwd())
        self.recipe = None  # temporary - remove in future

        self.compose_filepath = working_dir / "compose.yml"

        self.__sources = None
        self.__service_modules = None
        self.__infrastructure = None

        self.__spec = None

        self.__version_control = None
        self.__compose_spec = None

    def saturate(self, recipe_filepath="./recipe.toml"):
        recipe = Recipe.load(recipe_filepath)

        self.recipe = recipe  # temporary - remove in future

        self.__sources = ModelMap.generate(SourceModel, recipe.sources, parent=self)
        self.__service_modules = ModelMap.generate(
            ServiceModuleModel, recipe.service_modules, parent=self
        )
        self.__infrastructure = ModelMap.generate(
            InfrastructureModule, recipe.infrastructure, parent=self
        )

        self.__spec = recipe.solution

    @property
    def sources(self):
        if self.__sources is None:
            raise self.NotSaturated()
        return self.__sources

    @property
    def service_modules(self):
        if self.__service_modules is None:
            raise self.NotSaturated()
        return self.__service_modules

    @property
    def infrastructure(self):
        if self.__infrastructure is None:
            raise self.NotSaturated()
        return self.__infrastructure

    @property
    def spec(self):
        if self.__spec is None:
            raise self.NotSaturated()
        return self.__spec

    @property
    def version_control(self):
        if self.__version_control is None:
            self.__version_control = VersionControl(self)
        return self.__version_control

    @property
    def available_updates(self):
        return self.version_control.available_versions

    def module_iterator(self):
        return chain(iter(self.service_modules), iter(self.infrastructure))

    @property
    def compose_spec(self):
        if self.__compose_spec is None:
            self.__load_compose_spec()
        return self.__compose_spec

    def __load_compose_spec(self):
        try:
            with self.compose_filepath.open("r") as f:
                self.__compose_spec =  yaml.safe_load(f)
        except FileNotFoundError:
            self.__compose_spec = None

    def save_compose_spec(self, compose_definition):
        self.__compose_spec = compose_definition
        with self.compose_filepath.open("w") as f:
            yaml.safe_dump(
                compose_definition, f, default_flow_style=False, sort_keys=False
            )

    class NotSaturated(Exception):
        pass


class VersionControl:
    def __init__(self, solution):
        self.__solution = solution
        self.__implementation = SolutionGitVC
        self.__current_version = None
        self.__available_versions = None  # list with latest update at index 0

        self.__target_version = None

    @property
    def available_versions(self):
        if self.__available_versions is None:
            self.__get_version_data()
        return self.__available_versions

    @property
    def current_version(self):
        if self.__current_version is None:
            self.__get_version_data()
        return self.__current_version

    @property
    def target_version(self):
        return self.__target_version

    @target_version.setter
    def target_version(self, new_value):
        if new_value in self.available_versions:
            self.__target_version = new_value
        else:
            raise FatalError(
                f"Requested solution version of {new_value} is not one of the available versions: {self.available_versions}"
            )

    def can_update(self):
        return (
            len(self.available_versions) > 0
            and self.available_versions[0] != self.current_version
        )

    def __get_version_data(self):
        self.__current_version, self.__available_versions = (
            self.__implementation.fetch_version_details()
        )

    def update(self):
        updated = self.__implementation.do_update(self.target_version)
        if updated:
            self.__current_version = self.target_version
