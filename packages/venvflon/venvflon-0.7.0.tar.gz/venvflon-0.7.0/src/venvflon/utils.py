from __future__ import annotations

from collections.abc import Sequence
from enum import Enum
from os import sep, walk
from pathlib import Path
from re import search
from subprocess import CalledProcessError, run
from time import sleep


class LinkMode(Enum):
    """Mode to create symbolic link."""
    PYTHON = 'python.exe'
    PWSH5 = 'powershell.exe'
    PWSH7 = 'pwsh.exe'


LINK_MODE_MAP = {0: LinkMode.PYTHON, 5: LinkMode.PWSH5, 7: LinkMode.PWSH7}


def run_command(cmd: Sequence[str], cwd: Path | None = None) -> int:
    """
    Run command in shell as a subprocess.

    :param cmd: The command to be executed as a sequence of strings
    :param cwd: current working directory
    :return: The return code of command
    """
    try:
        proc = run(cmd, check=True, shell=False, cwd=cwd)
        return proc.returncode
    except CalledProcessError as e:
        print(f'Result: {e}')
        return -1


def get_command_output(cmd: Sequence[str], cwd: Path | None = None) -> tuple[int, str, str]:
    """
    Execute command and return its output.

    :param cmd: The command to be executed as a sequence of strings
    :param cwd: current working directory
    :return: Tuple with return code, stderr and stdout
    """
    try:
        result = run(cmd, capture_output=True, check=True, cwd=cwd)
        return result.returncode, result.stderr.decode('utf-8'), result.stdout.decode('utf-8')
    except CalledProcessError as e:
        print(f'Result: {e}')
        return e.returncode, e.stderr.decode('utf-8'), e.stdout.decode('utf-8')
    except (CalledProcessError, FileNotFoundError) as e:
        print(f'Result: {e}')
        return 255, 'None of venv were detected', ''


def make_sym_link(to_path: Path, target: Path, mode: LinkMode = LinkMode.PWSH5, timer: float = 1.2) -> None:
    """
    Make a symbolic link.

    :param to_path: Path to a symbolic link
    :param target: Target path
    :param mode: Method to create symbolic name
    :param timer: sleeping timer for PowerShell 5 and PowerShell 7 options
    """
    if mode == LinkMode.PYTHON:
        to_path.symlink_to(target=target, target_is_directory=True)
    else:
        cmd_symlink = f'"New-Item -ItemType SymbolicLink -Path \\"{to_path}\\" -Target \\"{target}\\"'
        ps_command = f"Start-Process {mode.value} -ArgumentList '-Command {cmd_symlink}' -Verb RunAs"
        print(f'Make symbolic link: {ps_command}')
        run_command(cmd=[mode.value, '-Command', ps_command])
        sleep(timer)


def rm_sym_link(sym_link: Path, mode: LinkMode = LinkMode.PWSH5) -> None:
    """
    Remove a symbolic link.

    :param sym_link: Path to a symbolic link
    :param mode: How to remove a symbolic link
    """
    if sym_link.exists():
        if mode == LinkMode.PYTHON:
            sym_link.unlink(missing_ok=True)
        else:
            rm_symlink = f"(Get-Item '{sym_link}').Delete()"
            ps_command = f'Start-Process {mode.value} -ArgumentList "-Command {rm_symlink}" -Verb RunAs'
            print(f'Execute: {ps_command}')
            run_command(cmd=[mode.value, '-Command', ps_command])


def venv_list_in(current_path: Path, max_depth: int = 1) -> list[Path]:
    """
    Find all virtual environments in a given path.

    :param current_path: Path to search in
    :param max_depth: Maximum depth of search
    :return: A list of paths to virtual environments
    """
    result = []
    for dir_path, dir_names, _ in walk(current_path, topdown=True):
        for dirname in dir_names:
            if '.venv_' in dirname:
                result.append(Path(dir_path) / dirname)
        if dir_path.count(sep) - str(current_path).count(sep) == max_depth - 1:
            del dir_names[:]
    return result


def extract_time(entry: str) -> float:
    """
    Extract a time value from a given text entry, converting it to milliseconds.

    Returns 0.0 if no valid time value is found in the input.

    :param entry: The input text from which to extract the time value.
    :return: The extracted time value in milliseconds.
    """
    if match:= search(r'(\d+(?:\.\d+)?)(ms|s)', entry):
        value, unit = match.groups()
        value = float(value)
        return value * 1000 if unit == 's' else value
    return 0.0


def extract_installed_packages(entry: Sequence[str]) -> int:
    """
    Extract the number of installed packages from a sequence of strings.

    The method searches each string in the sequence for a pattern that matches
    an indication of installed packages and then retrieves the number if found.
    The method stops processing once it finds the first valid match.

    :param entry: A sequence of strings that represent command output
    :return: The number of installed packages, if no match is found, it defaults to 0.
    """
    no_of_pack = 0
    for line in entry:
        if match:= search(r'Installed (\d+) package', line):
            no_of_pack = int(match.group(1))
            break
    return no_of_pack


def get_uv_pythons_list() -> list[str]:
    """
    Get a list of Python versions manged by uv.

    :return: A list of Python versions as strings
    """
    output = []
    *_, out = get_command_output(cmd=['uv', 'python', 'list'])

    for line in out.strip().splitlines():
        match = search(r'^cpython-([^-]+)-', line)
        if match:
            output.append(match.group(1))

    if len(output) > 1:
        output.pop(0)
    return output if len(output) > 1 else ['']
