from shoestring_assembler.constants import Contants
from pathlib import Path
from shoestring_assembler.schemas import MetaSchema, SchemaValidationError
from shoestring_assembler.views.interface.updates import FatalError
from shoestring_assembler.models.user_config import UserConfigTemplate

try:
    import tomllib as toml
except ImportError:
    import tomli as toml


class SourceModel:
    BASE_SOURCE_PATH = Path(f"./{Contants.MODULE_SOURCE_FILES_DIR}")
    BASE_CONFIG_PATH = Path(f"./{Contants.SOLUTION_CONFIG_DIR}")
    def __init__(self, name, spec, solution_model):
        self.__name = name
        self.__spec = spec

        # deferred loading
        self.__source_meta = None

        # File paths
        self.__relative_path = self.BASE_SOURCE_PATH / self.__name
        self.__meta_file_path = self.__relative_path / Contants.META_FILE_NAME

        self.solution_config_dir = self.BASE_CONFIG_PATH / name

    @property
    def name(self):
        return self.__name

    @property
    def spec(self):
        return self.__spec

    @property
    def relative_directory_path(self):
        return self.__relative_path

    @property
    def meta(self):
        if self.__source_meta is None:
            self.__source_meta = self.__load_meta()
        return self.__source_meta

    def __load_meta(self):
        try:
            with open(
                self.__meta_file_path,
                "rb",
                # description="Loading meta...",
            ) as file:
                meta = toml.load(file)
            # validate
            MetaSchema.validate(meta)
            return meta
        except FileNotFoundError:
            raise FatalError(
                f"Unable to find meta file for {self.__name}. Expected to find it at: {self.__meta_file_path}"
            )
        except SchemaValidationError as v_err:
            raise FatalError(
                f"Error in meta file for source '{self.__name}' at {v_err.json_path}:\n\n{v_err.message}\n" + 
                f"Meta file for source '{self.__name}' is not valid -- unable to start the solution"
            )