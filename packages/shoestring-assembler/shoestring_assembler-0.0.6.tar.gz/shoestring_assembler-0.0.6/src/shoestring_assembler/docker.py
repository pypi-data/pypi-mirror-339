import select
import subprocess
from shoestring_assembler.display import Display
from shoestring_assembler.models import SolutionModel

from pathlib import Path
import yaml


class Docker:
    @classmethod
    def build(cls, solution_model: SolutionModel):
        command = ["docker", "compose", "build"]
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out_buffer = bytearray()
        err_buffer = bytearray()
        while process.returncode == None:
            while True:
                out_line = None
                err_line = None
                no_stdout = False
                no_stderr = False

                read_list, _wlist, _xlist = select.select(
                    [process.stderr, process.stdout], [], [], 1
                )
                # Display.print_log(read_list,console=console)
                if process.stderr in read_list:
                    char = process.stderr.read(1)
                    if char == b"\n":
                        err_line = err_buffer.decode()
                        err_buffer.clear()
                    elif char:
                        # Display.print_log(f"echar: {char}")
                        err_buffer += char
                    else:
                        no_stdout = True  # end of file
                else:
                    no_stdout = True  # timeout - break to check if process terminated

                if process.stdout in read_list:
                    char = process.stdout.read(1)
                    if char == b"\n":
                        out_line = out_buffer.decode()
                        out_buffer.clear()
                    elif char:
                        # Display.print_log(f"ochar: {char}")
                        out_buffer += char
                    else:
                        no_stderr = True  # end of file
                else:
                    no_stderr = True  # timeout - break to check if process terminated

                if no_stdout and no_stderr:
                    break

                if out_line:
                    Display.print_log(f"[white]{out_line}", log_level=2)
                if err_line:
                    Display.print_complete(f"{err_line}")

            process.poll()

        process.wait()

        return process.returncode == 0

    @classmethod
    def setup_containers(cls, solution_model: SolutionModel):
        for service_name, service_spec in solution_model.compose_spec["services"].items():
            setup_cmd = service_spec.get("x-shoestring-setup-command")
            if setup_cmd:
                command = ["docker", "compose", "run","--rm", service_name]
                if isinstance(setup_cmd, list):
                    command.extend(setup_cmd)
                else:
                    command.append(setup_cmd)
                outcome = subprocess.run(command, capture_output=False)
                Display.print_log(outcome.returncode)

    @classmethod
    def start(cls):
        command = ["docker", "compose", "up", "-d", "--remove-orphans"]
        process = subprocess.Popen(command, stdout=None, stderr=None)
        process.wait()

        return process.returncode == 0
