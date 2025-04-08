from shoestring_assembler.constants import Contants
from pathlib import Path
from .base_module import BaseModule


class ServiceModuleModel(BaseModule):

    def __init__(self, name, spec,solution_model):
        super().__init__(name, spec, solution_model)
        self.type = "service_module"
