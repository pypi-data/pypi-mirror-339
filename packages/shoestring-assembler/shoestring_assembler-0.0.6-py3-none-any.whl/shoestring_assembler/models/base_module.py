from shoestring_assembler.models.source import SourceModel
from shoestring_assembler.models.container import Container
from .common import ModelMap
from shoestring_assembler.constants import Contants
from pathlib import Path

from .user_config import UserConfig

class BaseModule:

    def __init__(self, name: str, spec, solution_model):
        self.__name = name
        self.__spec = spec
        self.__source: SourceModel = solution_model.sources[spec["source"]]

        self.__containers = None
        self.__user_config = None

        self.data_dir_relpath = Path(f"./{Contants.DATA_DIR}/{self.__name}")

    @property
    def name(self) -> str:
        return self.__name

    @property
    def source(self) -> SourceModel:
        return self.__source

    @property
    def spec(self):
        return self.__spec

    @property
    def containers(self):
        if self.__containers is None:
            container_list = self.__spec.get("containers", [])
            container_map = {
                container_name: {
                    "ports": self.__spec.get("ports", {}).get(container_name, {}),
                    "alias": self.__spec.get("alias", {}).get(container_name, None),
                    "identifier": (
                        f"{self.name}-{container_name}"
                        if len(container_list) > 1
                        else self.name
                    ),
                }
                for container_name in container_list
            }

            self.__containers = ModelMap.generate(Container, container_map, parent=self)
        return self.__containers


    @property
    def user_config(self):
        if self.__user_config is None:
            self.__user_config = UserConfig(self)
        return self.__user_config
