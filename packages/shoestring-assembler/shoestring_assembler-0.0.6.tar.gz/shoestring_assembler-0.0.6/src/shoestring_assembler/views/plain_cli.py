CANCEL_PHRASE = "cancel"

from rich.prompt import Prompt, Confirm
from ..display import Display, OptionPrompt
from ..engine import step_definitions
from .interface import updates


from shoestring_assembler.models import SolutionModel, UserConfig

import sys


class PlainCLI:
    def __init__(self):
        self.do_prompt_for_next_phase = True

    def notify_fn(self, msg):
        match (msg):
            case updates.StageHeading():
                Display.print_top_header(msg.stage)

            case updates.StepHeading():
                Display.print_header(msg.step)

            case updates.InfoMsg():
                Display.print_log(msg.content, msg.detail_level)

            case updates.WarningMsg():
                Display.print_warning(msg.content)

            case updates.ErrorMsg():
                Display.print_error(msg.content)

            case updates.SuccessMsg():
                Display.print_complete(msg.content)

            case updates.DebugLog():
                Display.print_debug(msg.content)

            case updates.AttentionMsg():
                Display.print_notification(msg.content)

            case updates.NextStepsMsg():
                Display.print_next_steps(msg.content)

    def handle(self, step, solution_model: SolutionModel):
        match (step):
            case step_definitions.ChooseSolution():
                if len(step.provider_list) > 1:
                    key_list = []
                    name_list = []
                    for provider_key, provider_details in step.provider_list[
                        "providers"
                    ].items():
                        key_list.append(provider_key)
                        name_list.append(provider_details["name"])

                    provider_index = OptionPrompt.ask(
                        "select a provider", choices=name_list
                    )
                    provider = key_list[provider_index - 1]
                else:
                    provider = list(step.provider_list["providers"].keys())[0]

                solution_list = step.provider_list["providers"][provider]["solutions"]
                solution_index = OptionPrompt.ask(
                    "Select a provider",
                    choices=[solution["name"] for solution in solution_list],
                )
                solution = solution_list[solution_index - 1]
                step.resolve(solution)
            case step_definitions.ChooseSolutionVersion():
                version_index = OptionPrompt.ask(
                    "Select a version", choices=step.version_list, default=1
                )
                step.resolve(step.version_list[version_index - 1])
            case step_definitions.SelectUpdateVersion():
                Display.print_log("Which version do you want to update to?")
                version_index = OptionPrompt.ask(
                    "Select a version",
                    choices=solution_model.available_updates,
                    default=1,
                )
                solution_model.version_control.target_version = (
                    solution_model.available_updates[version_index - 1]
                )
                step.resolve()
            case step_definitions.GetConfigurationInputs():
                reconfiguring = False

                for service_module in solution_model.service_modules:
                    Display.print_header(
                        f"Setting up user config for {service_module.name}"
                    )

                    user_config = service_module.user_config
                    status = user_config.status

                    def log_status(outcome, colour="green"):
                        Display.print_log(
                            f"[{colour}]\[{outcome}][/{colour}] [white]{service_module.name}"
                        )

                    if status == UserConfig.Status.NO_TEMPLATE:
                        log_status("status")
                        continue

                    if not reconfiguring:
                        match (status):
                            case UserConfig.Status.WARN_FUTURE:
                                log_status("warning", "yellow")
                                Display.print_warning(
                                    f"Current user config version is {user_config.version} which is newer than the template version of {user_config.template.version}.\n"
                                    + f"[red]This might be ok! [/red] - but it should be checked!\n"
                                    + f"You can find the current user config files at [purple]./{user_config.rel_path}[/purple] and the template files at [purple]./{user_config.template.rel_path}[/purple]"
                                )
                                continue
                            case UserConfig.Status.MINOR_UPDATE:
                                log_status(status)
                                continue  # minor updates don't need reconfiguration
                            case UserConfig.Status.UP_TO_DATE:
                                log_status(status)
                                continue  # up to date - no config to be done
                            case _:
                                log_status(status)
                    else:
                        log_status("reconfigure")

                    user_config.requires_configuration = True
                    prompt_list = user_config.template.prompts

                    if prompt_list is None:
                        pass
                    else:
                        while len(prompt_list) > 0:
                            Display.print_debug(prompt_list)
                            prompt = prompt_list.pop(0)
                            key = prompt.get("key")
                            answer_key = prompt.get("answer_key", key)
                            if answer_key is None:
                                Display.print_warning(
                                    "Invalid prompt definition, unable to display.\n\nUser config might not generate properly"
                                )
                                continue

                            if "option" in prompt:
                                options = prompt["option"]
                                selected_index = OptionPrompt.ask(
                                    prompt["text"],
                                    choices=[option["prompt"] for option in options],
                                    default=user_config.prompt_defaults.get(answer_key),
                                )
                                Display.print_log(
                                    f"\[selected] {selected_index}", log_level=5
                                )
                                user_config.answers[answer_key] = selected_index
                                real_index = selected_index - 1  # revert to zero index

                                if "target" in options[real_index]:
                                    target_prompts = options[real_index]["target"]
                                    prompt_list = [*target_prompts, *prompt_list]
                                elif "value" in options[real_index]:
                                    selected_value = options[real_index]["value"]
                                    user_config.context[key] = selected_value
                            elif "value" in prompt:
                                user_config.context[key] = prompt.get("value")
                            else:
                                result = Prompt.ask(
                                    prompt["text"],
                                    default=user_config.prompt_defaults.get(answer_key),
                                )
                                Display.print_log(f"\[answered] {result}", log_level=5)
                                user_config.answers[answer_key] = result

                                user_config.context[key] = result

                step.resolve()

            case step_definitions.PromptToAssemble():
                if self.do_prompt_for_next_phase:
                    answer = Confirm.ask(
                        "? Do you want to assemble the solution now?", default=True
                    )
                else:
                    answer = True
                step.resolve(answer)
            case step_definitions.PromptToBuild():
                if self.do_prompt_for_next_phase:
                    answer = Confirm.ask(
                        "? Do you want to build the solution now?", default=True
                    )
                else:
                    answer = True
                step.resolve(answer)
            case step_definitions.PromptToStart():
                if self.do_prompt_for_next_phase:
                    answer = Confirm.ask(
                        "? Do you want to start the solution now?", default=True
                    )
                else:
                    answer = True
                step.resolve(answer)
            case _:
                pass

    def execute(self, engine):
        try:
            while True:
                next_ui_step = engine.next()
                if next_ui_step == None:
                    break
                self.handle(next_ui_step, engine.solution_model)
        except updates.FatalError as fatal_error:
            Display.print_error(fatal_error)
            sys.exit(255)
