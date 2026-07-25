from __future__ import annotations

import pytest
from pydantic import ValidationError

from tony.tools import (
    ToolArgument,
    ToolCapability,
    ToolMetadata,
    ToolResult,
)


def test_tool_metadata() -> None:
    metadata = ToolMetadata(
        name="mkdir",
        description="Create a directory",
        capability=ToolCapability.FILESYSTEM,
    )

    assert metadata.name == "mkdir"
    assert metadata.description == "Create a directory"
    assert metadata.capability is ToolCapability.FILESYSTEM


def test_tool_argument() -> None:
    argument = ToolArgument(
        name="path",
        value="/tmp/example",
    )

    assert argument.name == "path"
    assert argument.value == "/tmp/example"


def test_tool_result_success() -> None:
    result = ToolResult(
        success=True,
        output="Directory created.",
    )

    assert result.success is True
    assert result.output == "Directory created."
    assert result.error == ""
    assert result.exit_code == 0


def test_tool_result_failure() -> None:
    result = ToolResult(
        success=False,
        error="Permission denied.",
        exit_code=1,
    )

    assert result.success is False
    assert result.output == ""
    assert result.error == "Permission denied."
    assert result.exit_code == 1


def test_models_are_immutable() -> None:
    metadata = ToolMetadata(
        name="mkdir",
        description="Create a directory",
        capability=ToolCapability.FILESYSTEM,
    )

    with pytest.raises(ValidationError):
        metadata.name = "touch"
