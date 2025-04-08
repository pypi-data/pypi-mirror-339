from pathlib import Path
from shoestring_assembler.constants import Contants
from shoestring_assembler.views.interface.updates import FatalError
import json
import yaml
import re
from enum import Enum, unique


class UserConfigTemplate:
    def __init__(self, source):
        self.rel_path = Path(f"{Contants.USER_CONFIG_SRC_DIR}/{source.name}")
        self.abs_path = Path.resolve(Path.cwd()) / self.rel_path
        self.__template_management_dir = (
            self.abs_path / Contants.TEMPLATE_MANAGEMENT_SUBDIR
        )
        self.__version_file = (
            self.__template_management_dir / Contants.VERSION_FILE_NAME
        )
        self.__version_loaded = False
        self.__version = None

        self.__defaults_file = (
            self.__template_management_dir / Contants.DEFAULTS_FILE_NAME
        )
        self.__defaults = None

        self.__prompts_file = self.__template_management_dir / Contants.PROMPTS_FILE
        self.__prompts_loaded = False
        self.__prompts = None

    def exists(self):
        return self.abs_path.exists()

    @property
    def version(self):  # defers load till first use
        if not self.__version_loaded:
            self.__version = self.__load_version()
            self.__version_loaded = True
        return self.__version

    def __load_version(self):
        try:
            with self.__version_file.open(
                "r",
            ) as f:
                return Version(f.read())
        except FileNotFoundError:
            raise FatalError(
                f"Couldn't find version file in template directory. File expected at {self.version_file}."
            )
        except Version.Invalid:
            raise FatalError(f"The template version file contained an invalid version.")

    @property
    def defaults(self):  # defers load till first use
        if self.__defaults is None:
            self.__defaults = self.__load_defaults()
        return self.__defaults

    def __load_defaults(self):
        try:
            with self.__defaults_file.open("rb") as f:
                return json.load(f)
        except FileNotFoundError:
            return {}

    @property
    def prompts(self):  # defers load till first use
        if not self.__prompts_loaded:
            self.__prompts = self.__load_prompts()
            self.__prompts_loaded = True
        return self.__prompts

    def __load_prompts(self):
        try:
            with self.__prompts_file.open("rb") as f:
                return yaml.safe_load(f)
        except FileNotFoundError:
            return None


class UserConfig:

    @unique
    class Status(Enum):
        NO_TEMPLATE = "no_template"
        NOT_INITIALISED = "first_setup"
        MINOR_UPDATE = "minor_update"
        MAJOR_UPDATE = "major_update"
        WARN_FUTURE = "config_from_future"  # current version is higher than template
        UP_TO_DATE = "up_to_date"

    def __init__(self, service_module):
        self.__template = UserConfigTemplate(service_module.source)

        self.rel_path = Path(f"./{Contants.USER_CONFIG_DIR}/{service_module.name}")
        self.abs_path = Path.resolve(Path.cwd()) / self.rel_path
        self.__template_management_dir = (
            self.abs_path / Contants.TEMPLATE_MANAGEMENT_SUBDIR
        )

        self.__version_file = (
            self.__template_management_dir / Contants.VERSION_FILE_NAME
        )
        self.__version_loaded = False
        self.__version = None

        self.__prev_answers_file = (
            self.__template_management_dir / Contants.PREV_ANSWERS_FILE_NAME
        )
        self.__prev_answers = None

        self.__status = None

        self.requires_configuration = False
        self.answers = {}
        self.context = {}

    @property
    def template(self):
        return self.__template

    @property
    def version(self):  # defers load till first use
        if not self.__version_loaded:
            self.__version = self.__load_version()
            self.__version_loaded = True
        return self.__version

    @version.setter
    def version(self, new_value):
        with self.__version_file.open("w") as f_out:
            f_out.write(str(new_value))

    def __load_version(self):
        try:
            with self.__version_file.open(
                "r",
            ) as f:
                return Version(f.read())
        except FileNotFoundError:
            return None
        except Version.Invalid:
            raise FatalError(
                f"The user config version file contained an invalid version."
            )

    @property
    def status(self):
        if self.__status is None:
            self.__status = self.__get_status()
        return self.__status

    def __get_status(self):
        if not self.template.exists():  # there is no template
            return UserConfig.Status.NO_TEMPLATE

        # check template version - errors if format invalid or not found
        self.template.version

        # get user_config version from file - errors if format invalid
        # if not found then user config hasn't been set up - trigger setup
        if self.version == None:
            return UserConfig.Status.NOT_INITIALISED

        # compare versions and handle updates accordingly
        for index in range(2):
            if self.version[index] == self.template.version[index]:
                continue
            if self.version[index] < self.template.version[index]:
                match index:
                    case 0:  # major update
                        return UserConfig.Status.MAJOR_UPDATE
                    case 1:  # minor update
                        return UserConfig.Status.MINOR_UPDATE
            if self.version[index] > self.template.version[index]:
                return UserConfig.Status.WARN_FUTURE

        return UserConfig.Status.UP_TO_DATE

    @property
    def prev_answers(self):
        if self.__prev_answers is None:
            self.__prev_answers = self.__load_prev_answers()
        return self.__prev_answers

    @prev_answers.setter
    def prev_answers(self,new_value):
        with self.__prev_answers_file.open("w") as f:
            json.dump(new_value, f)

    def __load_prev_answers(self):
        try:
            with self.__prev_answers_file.open("rb") as f:
                return json.load(f)
                # prompt_defaults.update(prev_answers)
        except FileNotFoundError:
            return {}

    @property
    def prompt_defaults(self):
        return {**self.template.defaults, **self.prev_answers}


class Version(tuple):
    valid_regex = re.compile("^\s*(\d+)\.(\d+)\s*$")

    class Invalid(Exception):
        pass

    def __new__(cls, version_string):
        match = cls.valid_regex.match(version_string)
        if match is None:
            raise cls.Invalid(version_string)

        return super().__new__(cls, match.groups())

    def __init__(self, version_string):
        self.__version_string = version_string

    def __str__(self):
        return self.__version_string
