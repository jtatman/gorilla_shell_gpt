import os
import platform
import shlex
from enum import Enum
from tempfile import NamedTemporaryFile
from typing import Any, Callable

import typer
from click import BadParameter


class ModelOptions(str, Enum):
    """
    Model endpoint compatibility
    https://platform.openai.com/docs/models/model-endpoint-compatibility
    """

    GPT4 = "gpt-4"
    GPT4_PREVIEW = "gpt-4-1106-preview"
    GPT432k = "gpt-4-32k"
    GPT35TURBO1106 = "gpt-3.5-turbo-1106"
    GPT34TURBO = "gpt-3.5-turbo"
    GPT35TURBO16K = "gpt-3.5-turbo-16k"
    GPT35TURBOINSTRUCT = "gpt-3.5-turbo-instruct"
    


def get_edited_prompt() -> str:
    """
    Opens the user's default editor to let them
    input a prompt, and returns the edited text.

    :return: String prompt.
    """
    with NamedTemporaryFile(suffix=".txt", delete=False) as file:
        # Create file and store path.
        file_path = file.name
    editor = os.environ.get("EDITOR", "vim")
    # This will write text to file using $EDITOR.
    os.system(f"{editor} {file_path}")
    # Read file when editor is closed.
    with open(file_path, "r", encoding="utf-8") as file:
        output = file.read()
    os.remove(file_path)
    if not output:
        raise BadParameter("Couldn't get valid PROMPT from $EDITOR")
    return output


def run_command(command: str) -> None:
    """
    Runs a command in the user's shell.
    It is aware of the current user's $SHELL.
    :param command: A shell command to run.
    """
    if platform.system() == "Windows":
        is_powershell = len(os.getenv("PSModulePath", "").split(os.pathsep)) >= 3
        full_command = (
            f'powershell.exe -Command "{command}"'
            if is_powershell
            else f'cmd.exe /c "{command}"'
        )
    else:
        shell = os.environ.get("SHELL", "/bin/sh")
        full_command = f"{shell} -c {shlex.quote(command)}"

    os.system(full_command)


def option_callback(func: Callable) -> Callable:  # type: ignore
    def wrapper(cls: Any, value: str) -> None:
        if not value:
            return
        func(cls, value)
        raise typer.Exit()

    return wrapper


@option_callback
def install_shell_integration(*_args: Any) -> None:
    """
    Installs shell integration. Currently only supports Linux.
    Allows user to get shell completions in terminal by using hotkey.
    Allows user to edit shell command right away in terminal.
    """
    # TODO: Add support for Windows.
    # TODO: Implement updates.
    if platform.system() == "Windows":
        typer.echo("Windows is not supported yet.")
    else:
        url = "https://raw.githubusercontent.com/TheR1D/shell_gpt/shell-integrations/install.sh"
        os.system(f'sh -c "$(curl -fsSL {url})"')
