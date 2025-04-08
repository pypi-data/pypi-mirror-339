import rich.progress
from pathlib import Path
import subprocess
import re
import select
import os

from .display import Display
from .constants import Contants


class GetSolutionUsingGit:
    remote_tag_search_regex = re.compile("^\w*\trefs/tags/(?P<tag>[\w\d\.-]*)\s*")
    strict_tag_regex = re.compile("^v(\d*)\.(\d*)\.(\d*)$")

    @classmethod
    def download(cls, selected):
        Display.print_header(f"Downloading {selected['name']}")
        tag_or_branch = selected["tag"] if "tag" in selected else selected["branch"]

        env = os.environ.copy()
        env["GIT_TERMINAL_PROMPT"] = (
            "0"  # prevents hanging on username input if url invalid
        )

        command = [
            "git",
            "clone",
            "--progress",  # force inclusion of progress updates
            "--branch",
            tag_or_branch,
            selected["url"],
        ]

        Display.print_debug(f"command: {command}")

        process = subprocess.Popen(
            command, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE, env=env
        )  # git outputs updates over stderr

        with rich.progress.Progress(transient=True) as progress:
            git_clone_progress_bars(process, progress, progress.console)

        return process.returncode == 0

    @classmethod
    def available_versions(cls, url, minimum_version):
        minimum_vsn_tuple = cls.strict_tag_regex.match(minimum_version).groups()
        env = os.environ.copy()
        env["GIT_TERMINAL_PROMPT"] = (
            "0"  # prevents hanging on username input if url invalid
        )
        command = ["git", "ls-remote", "--tags", "--sort=-version:refname", url]
        result = subprocess.run(command, capture_output=True, env=env)
        readout = result.stdout.decode()

        tag_entries = []
        for line in readout.split("\n"):
            tags = cls.remote_tag_search_regex.findall(line)

            for tag in tags:
                match = cls.strict_tag_regex.match(tag)
                if match:
                    if match.groups() >= minimum_vsn_tuple:
                        tag_entries.append(tag)

        return tag_entries


class SolutionGitVC:
    head_search_regex = re.compile("[^/](?P<has_head>HEAD)")  # TODO: may need some work
    tag_search_regex = re.compile("(?:tag:\s?(?P<tag>[\w\d\.-]*))")
    strict_tag_regex = re.compile("^v\d*\.\d*\.\d*$")

    @classmethod
    def _fetch_updates(cls):
        env = os.environ.copy()
        env["GIT_TERMINAL_PROMPT"] = (
            "0"  # prevents hanging on username input if url invalid
        )

        # fetch updates
        command = [
            "git",
            "fetch",
            "--progress",
            "--all",
        ]
        Display.print_log("Fetching list of available versions...", log_level=2)
        result = subprocess.run(command, capture_output=True, env=env)
        Display.print_debug(
            f"git fetch return code: {result.returncode}\nstdout:\n{result.stdout.decode()}\nstderr:\n{result.stderr.decode()}"
        )

        if result.returncode != 0:
            Display.print_warning(
                "Unable to fetch the latest list of available versions"
            )

    @classmethod
    def fetch_version_details(cls, strict_tags_only=True, full_list=True):
        cls._fetch_updates()

        env = os.environ.copy()
        env["GIT_TERMINAL_PROMPT"] = (
            "0"  # prevents hanging on username input if url invalid
        )

        # get current version
        command = ["git", "describe", "--exact-match", "--tags"]
        result = subprocess.run(command, capture_output=True, env=env)
        current_version = result.stdout.decode().strip()

        # check tags
        command = [
            "git",
            "log",
            "--all",  # include all commits
            '--format="%D"',  # print list of commit refs (includes HEAD, tags and branches)
            "--simplify-by-decoration",  # filter out commits that have empty ref entries
        ]
        result = subprocess.run(command, capture_output=True, env=env)
        readout = result.stdout.decode()

        tag_entries = []
        for line in readout.split("\n"):
            has_head = cls.head_search_regex.search(line)
            tags = cls.tag_search_regex.findall(line)

            if strict_tags_only:
                tags = [tag for tag in tags if cls.strict_tag_regex.match(tag)]

            if tags:
                tag_entries.extend(
                    [
                        {
                            "has_head": has_head is not None,
                            "tag": tag,
                        }
                        for tag in tags
                    ]
                )
            elif has_head:
                tag_entries.append(
                    {
                        "has_head": has_head is not None,
                        "tag": None,
                    }
                )

        Display.print_debug(f"raw:\n{readout}\nextracted:\n{tag_entries}")
        Display.print_log("Solution versions:")
        first_current = None
        for index, entry in enumerate(tag_entries):
            is_current = (
                entry["tag"] == current_version
                if current_version
                else entry["has_head"]
            )
            if is_current:
                first_current = index
            else:
                if not full_list and first_current is not None:
                    # only show one entry prior to (current) entry
                    Display.print_log("...")
                    break

            tag_display = (
                f'[purple]{entry["tag"]} [/purple]'
                if entry["tag"]
                else f"[white]none[/white]"
            )

            Display.print_log(
                f'{tag_display} [green]{"(current)"if is_current else " "}'
            )

        current_version = (
            current_version if current_version else None
        )  # converts "" to None
        available_updates = [entry["tag"] for entry in tag_entries[0:first_current]]

        return current_version, available_updates

    @classmethod
    def do_update(cls, tag_or_branch):

        env = os.environ.copy()
        env["GIT_TERMINAL_PROMPT"] = (
            "0"  # prevents hanging on username input if url invalid
        )

        command = ["git", "checkout", tag_or_branch]

        Display.print_debug(f"command: {command}")

        process = subprocess.Popen(
            command, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE, env=env
        )  # git outputs updates over stderr

        # likely overkill but would be good to be able to relay updates
        buffer = bytearray()
        while process.returncode == None:
            while True:
                line = None

                read_list, _wlist, _xlist = select.select([process.stderr], [], [], 1)
                # Display.print_log(read_list,console=console)
                if process.stderr in read_list:
                    char = process.stderr.read(1)
                    if char == b"\n":
                        line = buffer.decode()
                        buffer.clear()
                    elif char:
                        # Display.print_log(f"char: {char}", console=console)
                        buffer += char
                    else:
                        break  # end of file
                else:
                    break  # timeout - break to check if process terminated

                if line:
                    Display.print_log(f"[white]{line}")
                else:
                    pass

            process.poll()

        if process.returncode == 0:
            Display.print_complete("Update Complete.")
        else:
            Display.print_error("Update failed.")

        return process.returncode == 0


class GitSource:

    @staticmethod
    def fetch(name, details, console, progress: rich.progress.Progress):
        tag = details.get("tag")
        branch = details.get("branch")
        path = details["path"]  # could throw error but shouldn't due to validation

        dest_path = Path.resolve(Path.cwd()) / Contants.MODULE_SOURCE_FILES_DIR / name

        num_slashes = path.count("/")
        if num_slashes == 0:
            url = f"https://github.com/DigitalShoestringSolutions/{path}"
        elif num_slashes == 1:
            url = f"https://github.com/{path}"
        else:
            url = path

        Display.print_log(
            f"type: git, repo: {url} target:{ f'tag {tag}' if tag else f' branch {branch}'}",
            console=console,
        )

        env = os.environ.copy()
        env["GIT_TERMINAL_PROMPT"] = (
            "0"  # prevents hanging on username input if url invalid
        )

        command = [
            "git",
            "clone",
            "--progress",  # force inclusion of progress updates
            "--depth",
            "1",  # only download latest commit - no history (massive speed up)
            "--branch",
            tag if tag else branch,
            url,
            dest_path,
        ]

        Display.print_debug(f"command: {command}", console=console)

        process = subprocess.Popen(
            command, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE, env=env
        )  # git outputs updates over stderr

        git_clone_progress_bars(process, progress, console)

        return process.returncode == 0


# display utilities


def git_clone_progress_bars(process, progress: rich.progress.Progress, console):
    # likely overkill but would be good to be able to relay updates
    buffer = bytearray()
    active_progress_tracker = None
    regex = re.compile("^(?P<label>.*)\d+% \((?P<progress>\d*)/(?P<total>\d*)\).*")
    while process.returncode == None:
        while True:
            line = None
            line_update = False

            read_list, _wlist, _xlist = select.select([process.stderr], [], [], 1)
            # Display.print_log(read_list,console=console)
            if process.stderr in read_list:
                char = process.stderr.read(1)
                if char == b"\r" or char == b"\n":
                    if char == b"\r":
                        line_update = True
                    line = buffer.decode()
                    buffer.clear()
                elif char:
                    # Display.print_log(f"char: {char}", console=console)
                    buffer += char
                else:
                    break  # end of file
            else:
                break  # timeout - break to check if process terminated

            if line:
                if active_progress_tracker or line_update:  # progress update line
                    m = regex.match(line)
                    if active_progress_tracker is not None:
                        if line_update:  # update
                            progress.update(
                                active_progress_tracker,
                                description=m.group("label"),
                                completed=int(m.group("progress")),
                            )
                        else:  # end
                            if m:
                                progress.update(
                                    active_progress_tracker,
                                    completed=int(m.group("progress")),
                                )
                            else:
                                progress.update(active_progress_tracker, advance=100000)
                            progress.stop_task(active_progress_tracker)
                            progress.remove_task(active_progress_tracker)
                            active_progress_tracker = None
                            Display.print_log(
                                f"[white]{line}", console=console, log_level=2
                            )
                    elif line_update:  # new
                        active_progress_tracker = progress.add_task(
                            m.group("label"),
                            start=True,
                            completed=int(m.group("progress")),
                            total=int(m.group("total")),
                        )
                else:  # normal line
                    Display.print_log(f"[white]{line}", console=console, log_level=2)
            else:
                pass

        process.poll()
