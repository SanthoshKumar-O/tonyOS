"""Tests for the argument validator."""

from __future__ import annotations

from tony.tools import (
    ArgumentValidator,
    ToolArgument,
    ToolSelection,
)


def create_selection() -> ToolSelection:
    """Create a tool selection for testing."""

    return ToolSelection(
        tool_name="pwd",
        confidence=1.0,
        reason="Test",
    )


def test_validate_valid_arguments() -> None:
    validator = ArgumentValidator()

    result = validator.validate(
        create_selection(),
        [
            ToolArgument(
                name="path",
                value="/home/user",
            ),
        ],
    )

    assert result.valid is True
    assert result.reason == "Arguments are valid."


def test_validate_empty_arguments() -> None:
    validator = ArgumentValidator()

    result = validator.validate(
        create_selection(),
        [],
    )

    assert result.valid is True
    assert result.reason == "Arguments are valid."


def test_validate_empty_argument_name() -> None:
    validator = ArgumentValidator()

    result = validator.validate(
        create_selection(),
        [
            ToolArgument(
                name="",
                value="/home/user",
            ),
        ],
    )

    assert result.valid is False
    assert result.reason == "Argument name cannot be empty."


def test_validate_empty_argument_value() -> None:
    validator = ArgumentValidator()

    result = validator.validate(
        create_selection(),
        [
            ToolArgument(
                name="path",
                value="",
            ),
        ],
    )

    assert result.valid is False
    assert result.reason == "Argument 'path' cannot be empty."
