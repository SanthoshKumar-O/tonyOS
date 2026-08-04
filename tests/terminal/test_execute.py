"""Tests for ExecuteCommandTool."""

from __future__ import annotations

from tony.tools import ToolArgument
from tony.tools.terminal import ExecuteCommandTool


def test_metadata() -> None:
    tool = ExecuteCommandTool()

    assert tool.metadata.name == "execute"


def test_requires_command() -> None:
    tool = ExecuteCommandTool()

    result = tool.execute([])

    assert result.success is False
    assert result.error == "Command is required."


def test_execute_echo() -> None:
    tool = ExecuteCommandTool()

    result = tool.execute(
        [
            ToolArgument(
                name="command",
                value="echo",
            ),
            ToolArgument(
                name="text",
                value="hello",
            ),
        ],
    )

    assert result.success is True
    assert result.output == "hello"
