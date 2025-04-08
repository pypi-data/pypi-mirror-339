from shoestring_assembler.assembler import Assembler
from shoestring_assembler.user_config import UserConfig
from shoestring_assembler.git import GetSolutionUsingGit, SolutionGitVC
from shoestring_assembler.filesystem import SolutionFilesystem
from shoestring_assembler.docker import Docker
from shoestring_assembler.views.interface.updates import (
    StageHeading,
    StepHeading,
    DebugLog,
    WarningMsg,
    FatalError,
    AttentionMsg,
    SuccessMsg,
)
from shoestring_assembler.models.solution import SolutionModel

import time
import os
import urllib
import yaml

from shoestring_assembler.engine import step_definitions as steps


class Engine:

    def __init__(self, update_callback, do_load_sources=True):
        self.do_load_sources = do_load_sources
        self.__solution_model = SolutionModel()

        self.__current_step: steps.ProcessStep = None

        self.update_ui = update_callback

    @property
    def solution_model(self):
        return self.__solution_model

    def init_download(self):
        self.__current_step = steps.FetchProvidedSolutionsList()

    def init_update(self):
        self.__current_step = steps.CheckForUpdates()

    def init_assemble(self):
        self.__current_step = steps.AssembleSolution()

    def init_reconfigure(self):
        self.__current_step = steps.GetConfigurationInputs()

    def init_setup(self):
        self.__current_step = steps.SetupSolution()

    def init_build(self):
        self.__current_step = steps.BuildSolution()

    def init_start(self):
        self.__current_step = steps.StartSolution()

    def next(self):
        next_ui_step = None
        while next_ui_step is None:
            self.update_ui(
                DebugLog(f"current step: {type(self.__current_step).__name__}")
            )
            try:
                if self.__current_step.is_resolved:
                    self.__current_step = self.__current_step.next_step
            except steps.ProcessStep.NotResolvedException:
                self.update_ui(
                    WarningMsg(
                        f"Step {type(self.__current_step).__name__} didn't resolve the first time"
                    )
                )
            finally:
                self.update_ui(
                    DebugLog(f"next step: {type(self.__current_step).__name__}")
                )
                if isinstance(self.__current_step, steps.EngineStep):
                    self.__handle_engine_step(self.__current_step)
                elif isinstance(self.__current_step, steps.Terminate):
                    break
                else:
                    next_ui_step = self.__current_step

            # time.sleep(1)
        return next_ui_step

    def __handle_engine_step(self, step):
        # Note each step should be resolved when the end of this function is reached
        resolution_args = []
        match (step):
            case steps.FetchProvidedSolutionsList():
                provider_list = self.fetch_available_solution_list()
                resolution_args = [provider_list]
            case steps.FetchAvailableSolutionVersions():
                available_versions = self.fetch_available_solution_versions(
                    step.solution_details
                )
                resolution_args = [available_versions]
            case steps.DownloadSolution():
                self.download_solution(step.solution_spec)
            case steps.AssembleSolution():
                self.assemble_solution()
            case steps.ConfigureSolution():
                self.configure()
            case steps.BuildSolution():
                self.build()
            case steps.CheckIfSetup():
                is_setup = self.check_setup()
                resolution_args = [is_setup]
            case steps.SetupSolution():
                self.setup()
            case steps.StartSolution():
                self.start()
            case steps.CheckForUpdates():
                can_update = self.check_for_updates()
                resolution_args = [can_update]
            case steps.DownloadUpdate():
                self.download_update()

        step.resolve(*resolution_args)

    ### process steps
    def fetch_available_solution_list(self):
        list_branch = os.getenv("SHOESTRING_LIST_BRANCH", "main")
        try:
            with urllib.request.urlopen(
                f"https://github.com/DigitalShoestringSolutions/solution_list/raw/refs/heads/{list_branch}/list.yaml"
            ) as web_in:
                content = web_in.read()
                provider_list = yaml.safe_load(content)
        except urllib.error.URLError:
            raise FatalError("Unable to fetch latest solution list")
        return provider_list

    def fetch_available_solution_versions(self, solution_details):
        available_versions = GetSolutionUsingGit.available_versions(
            solution_details["url"], solution_details["minimum_version"]
        )
        return available_versions

    def download_solution(self, selected):
        # if GetSolutionUsingGit.download(selected):
        #     Display.print_complete("Done")
        #     Display.print_next_steps(
        #         "* Move to the solution folder using [white]cd[/white]\n\n"
        #         + "* Once in the folder assemble the solution using [white]shoestring assemble[/white]"
        #     )
        # else:
        #     Display.print_error("Unable to download solution")
        pass

    def check_for_updates(self):
        self.update_ui(StageHeading("Update Solution"))
        self.update_ui(StepHeading("Checking for updates"))
        if self.solution_model.version_control.can_update():
            self.update_ui(AttentionMsg("New Updates are available."))
            return True
        else:
            self.update_ui(SuccessMsg("Already using the latest update."))
            return False

    def download_update(self):
        self.update_ui(
            StepHeading(
                f"Downloading update {self.solution_model.version_control.target_version}"
            )
        )
        self.solution_model.version_control.update()

    def assemble_solution(self):
        self.update_ui(StageHeading("Assembling Solution"))
        self.solution_model.saturate()
        SolutionFilesystem.verify(
            self.solution_model, check_sources=not self.do_load_sources
        )
        SolutionFilesystem.clean(clean_sources=self.do_load_sources)
        Assembler(self.solution_model).load_sources(do_gather=self.do_load_sources)
        Assembler(self.solution_model).generate_compose_file()

    def configure(self):
        UserConfig.configure(self.solution_model)

    def build(self):
        built = Docker.build(self.solution_model)
        if built:
            self.update_ui(SuccessMsg("Solution Built"))
        else:
            raise FatalError("Solution Building Failed")

    def check_setup(self):
        return False

    def setup(self):
        Docker.setup_containers(self.solution_model)

    def start(self):
        started = Docker.start()
        if started:
            self.update_ui(SuccessMsg("Solution is now running in the background"))

    def stop(self):
        pass
