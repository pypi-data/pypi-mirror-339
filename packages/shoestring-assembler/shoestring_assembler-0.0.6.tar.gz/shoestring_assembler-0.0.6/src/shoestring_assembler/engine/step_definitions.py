class ProcessStep:
    class NotResolvedException(Exception):
        pass

    def __init__(self):
        self.__resolved = False
        self.__next = None

    @property
    def is_resolved(self):
        return self.__resolved

    def resolve(self, next_step):
        self.__resolved = True
        self.__next = next_step

    def reset(self):
        self.__resolved = False

    @property
    def next_step(self):
        if not self.__resolved:
            raise ProcessStep.NotResolvedException()
        return self.__next


class UIStep(ProcessStep):
    pass


class EngineStep(ProcessStep):
    pass


class Terminate(ProcessStep):
    pass


class FetchProvidedSolutionsList(EngineStep):
    def __init__(self):
        super().__init__()

    def resolve(self, provider_list):
        if provider_list:
            super().resolve(ChooseSolution(provider_list))


class ChooseSolution(UIStep):
    def __init__(self, provider_list):
        super().__init__()
        self.provider_list = provider_list

    def resolve(self, selected_solution_details):
        if selected_solution_details:
            super().resolve(FetchAvailableSolutionVersions(selected_solution_details))


class FetchAvailableSolutionVersions(EngineStep):

    def __init__(self, solution_details):
        super().__init__()
        self.solution_details = solution_details

    def resolve(self, available_versions_list):
        if available_versions_list:
            super().resolve(
                ChooseSolutionVersion(self.solution_details, available_versions_list)
            )


class ChooseSolutionVersion(UIStep):

    def __init__(self, solution_details, version_list):
        super().__init__()
        self.solution_details = solution_details
        self.version_list = version_list

    def resolve(self, selected_version):
        if selected_version:
            super().resolve(DownloadSolution(selected_version))


class DownloadSolution(EngineStep):
    def __init__(self, solution_spec):
        super().__init__()
        self.solution_spec = solution_spec

    def resolve(self):
        super().resolve(PromptToAssemble())


class PromptToAssemble(UIStep):
    def resolve(self, do_assemble):
        if do_assemble:
            super().resolve(AssembleSolution())
        else:
            super().resolve(Terminate())


class AssembleSolution(EngineStep):
    def resolve(self):
        return super().resolve(GetConfigurationInputs())


class GetConfigurationInputs(UIStep):
    def resolve(self):
        super().resolve(ConfigureSolution())


class ConfigureSolution(EngineStep):
    def resolve(self):
        return super().resolve(PromptToBuild())


class PromptToBuild(UIStep):
    def resolve(self, do_build):
        if do_build:
            super().resolve(BuildSolution())
        else:
            super().resolve(Terminate())


class BuildSolution(EngineStep):
    def resolve(self):
        return super().resolve(CheckIfSetup())


class CheckIfSetup(EngineStep):
    def resolve(self, is_setup):
        if not is_setup:
            super().resolve(SetupSolution())
        else:
            super().resolve(PromptToStart())


class SetupSolution(EngineStep):
    def resolve(self):
        return super().resolve(PromptToStart())


class PromptToStart(UIStep):
    def resolve(self, do_start):
        if do_start:
            super().resolve(StartSolution())
        else:
            super().resolve(Terminate())


class StartSolution(EngineStep):
    def resolve(self):
        return super().resolve(Terminate())


class CheckForUpdates(EngineStep):
    def resolve(self,can_update):
        if can_update:
            return super().resolve(SelectUpdateVersion())
        else:
            return super().resolve(Terminate())

class SelectUpdateVersion(UIStep):
    def resolve(self):
        return super().resolve(DownloadUpdate())

class DownloadUpdate(EngineStep):
    def resolve(self):
        return super().resolve(PromptToAssemble())
