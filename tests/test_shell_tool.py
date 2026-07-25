from __future__ import annotations

import shutil

from tony.tools import ToolArgument
from tony.tools.shell import ShellTool


def test_shell_pwd() -> None:
    tool = ShellTool()

    result = tool.execute(
        [
            ToolArgument(
                name="command",
                value="pwd",
            ),
        ],
    )

    assert result.success is True
    assert result.output != ""
    assert result.exit_code == 0


def test_shell_python_version() -> None:
    tool = ShellTool()

    result = tool.execute(
        [
            ToolArgument(
                name="command",
                value="python3",
            ),
            ToolArgument(
                name="arg",
                value="--version",
            ),
        ],
    )

    assert result.success is True
    assert "Python" in (result.output + result.error)


def test_shell_missing_command() -> None:
    tool = ShellTool()

    result = tool.execute(
        [
            ToolArgument(
                name="command",
                value="does-not-exist",
            ),
        ],
    )

    assert result.success is False
    assert result.output == ""
    assert result.error != ""


def test_shell_without_arguments() -> None:
    tool = ShellTool()

    result = tool.execute([])

    assert result.success is False
    assert result.error == "A command is required."


def test_shell_metadata() -> None:
    tool = ShellTool()

    metadata = tool.metadata

    assert metadata.name == "shell"
    assert metadata.capability.value == "shell"


def test_shell_timeout() -> None:
    tool = ShellTool()

    sleep_command = shutil.which("sleep")

    if sleep_command is None:
        return

    result = tool.execute(
        [
            ToolArgument(
                name="command",
                value=sleep_command,
            ),
            ToolArgument(
                name="seconds",
                value="35",
            ),
        ],
    )

    assert result.success is False
    assert result.error == "Command execution timed out."
    assert result.exit_code == 124
