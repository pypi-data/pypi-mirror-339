from .base_module import BaseModule


class InfrastructureModule(BaseModule):

    def __init__(self, name, spec, solution_model):
        super().__init__(name, spec, solution_model)
        self.type = "infrastructure"
