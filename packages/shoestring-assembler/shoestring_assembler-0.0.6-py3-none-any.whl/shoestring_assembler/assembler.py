import rich.progress
import sys
from pathlib import Path
import yaml

from .display import Display


from .utilities import minimal_mustache
from .constants import Contants
from .filesystem import FilesystemSource
from .git import GitSource
from shoestring_assembler.views.interface.updates import FatalError

# import for typing
from shoestring_assembler.models import SolutionModel, ServiceModuleModel, BaseModule


class Assembler:

    def __init__(self, solution_model: SolutionModel):
        self.solution_model = solution_model

    def load_sources(self, do_gather):
        Display.print_header("Gathering Service Module Sources")

        if not do_gather:
            Display.print_complete(
                "Fetching service module sources disabled by command line arguements"
            )
        else:
            with (
                rich.progress.Progress() as progress
            ):  # displays progress bar on console

                used_sources = {module.source for module in self.solution_model.module_iterator()}  # this is a set, not a dict to prevent duplicates

                task = progress.add_task(
                    "[cyan]  Gathering Service Module Sources",
                    total=len(used_sources)
                )

                for source in used_sources:
                    Display.print_log(
                        f"Fetching {source.name}", console=progress.console
                    )

                    if "file" in source.spec:
                        result = FilesystemSource.fetch(
                            source.name,
                            source.spec["file"],
                            console=progress.console,
                        )
                    elif "git" in source.spec:
                        result = GitSource.fetch(
                            source.name,
                            source.spec["git"],
                            console=progress.console,
                            progress=progress,
                        )
                    else:
                        # this should never happen due to recipe validation
                        raise FatalError(
                            f"Source {source.name} does not include details on where to get it",
                            console=progress.console,
                        )

                    if result:
                        Display.print_complete(
                            f"Fetched '{source.name}' ", console=progress.console
                        )
                        progress.update(task, advance=1)  # updates progress bar
                    else:
                        progress.update(task, visible=False)
                        raise FatalError(
                            f"An error occured while fetching '{source.name}'",
                            console=progress.console,
                        )

            Display.print_complete("All Service Module Sources Gathered")

    def generate_compose_file(self):
        Display.print_header("Generating Compose File")
        compose_definition = {
            "services": {},
            "networks": {Contants.DOCKER_NETWORK_NAME: {"name": "shoestring-internal"}},
        }

        for service_module in self.solution_model.service_modules:
            service_set = self.generate_docker_services_for_module(
                service_module
            )
            compose_definition["services"].update(service_set)

        for infrastructure_module in self.solution_model.infrastructure:
            service_set = self.generate_docker_services_for_module(
                infrastructure_module
            )
            compose_definition["services"].update(service_set)

        compose_definition["x-shoestring"] = {
            "recipe": {
                "filename": self.solution_model.recipe._filepath_provided,
                "hash": self.solution_model.recipe._hash,
            }
        }

        self.solution_model.save_compose_spec(compose_definition)

        Display.print_complete(f"Compose file complete")

    def generate_docker_services_for_module(self, module: BaseModule):
        Display.print_log(f"[cyan]*  {module.name}")
        module_services = {}

        for container in module.containers:
            if len(module.containers) > 1:
                Display.print_log(f"[cyan]**  {container.identifier}")

            # form base
            service_definition = {
                "build": {
                    "context": str(module.source.relative_directory_path),
                    "dockerfile": f"./{container.meta.get('dockerfile','Dockerfile')}",
                    "additional_contexts": [
                        f"solution_config={module.source.solution_config_dir}"
                    ],
                },
                "networks": {
                    Contants.DOCKER_NETWORK_NAME: {
                        "aliases": [f"{container.alias}{Contants.DOCKER_ALIAS_SUFFIX}"]
                    }
                },
                "logging": {
                    "driver": "syslog",
                    "options": {"tag": f"docker-{container.identifier}"},
                },
                "labels": {
                    "net.digitalshoestring.solution": self.solution_model.spec["slug"],
                    "net.digitalshoestring.function": module.type,
                },
                "restart": "unless-stopped",
            }
            # extend with partials
            raw_partials_string = container.partial_compose_snippet
            if raw_partials_string:
                template_applied_string = minimal_mustache.render(
                    raw_partials_string, module.spec.get("template", {})
                )
                partials = yaml.safe_load(template_applied_string)
            else:
                partials = {}

            service_definition = {
                **partials,
                **service_definition,
            }  # update in this way to prevent partials from overwriting service_definition keys

            # sort out volumes
            # volumes = {
            #     "data": {"host": f"./{Contants.DATA_DIR}/{module.name}"},
            #     "user_config": {"host": f"./{Contants.USER_CONFIG_DIR}/{module.name}"},
            # }  # defaults
            
            container.volumes.apply_container_spec(container.meta.get("volume", {}))

            compose_volumes = []
            for volume in container.volumes.values():
                if volume.ignored: # container doesn't use this volume
                    continue
                volume.check_valid()  # throws errors if problems exist
                compose_volumes.append(volume.formatted())
                
            if len(compose_volumes) > 0:
                service_definition["volumes"] = compose_volumes

            # map in ports
            ports = {}  # defaults

            # map in container ports
            container_ports = container.meta.get("ports", {})
            for name, port_number in container_ports.items():
                if name not in ports:
                    ports[name] = {}
                ports[name]["container"] = port_number
            # map in host ports
            for name, port_number in container.host_ports.items():
                if name not in ports:
                    ports[name] = {}
                ports[name]["host"] = port_number

            # combine mappings
            compose_ports = []
            for name, mapping in ports.items():
                has_host = "host" in mapping
                has_cnt = "container" in mapping
                if has_host and has_cnt:  # everything as expected
                    entry = f'{mapping["host"]}:{mapping["container"]}'
                    compose_ports.append(entry)
                elif has_host:
                    # no container entry to map to
                    raise FatalError(
                        f"No corresponding container entry for port {name} of {container.identifier}."
                    )
                elif has_cnt:
                    # no host entry to map to
                    raise FatalError(
                        f"No corresponding host entry for port {name} of {container.identifier}."
                    )
            if len(compose_ports) > 0:
                service_definition["ports"] = compose_ports

            module_services[container.identifier] = service_definition

        return module_services


"""
TO DO List:
* work out what clean means
* handle volumes in snippets
* setup scripts

Longer term
* solution config templates & bootstrapping
* host side volume specification
* named volumes - when only has container entry?
    * would need warning if repeated
* Environment variables
* coveying port and alias mappings to services
*   external resources
"""
