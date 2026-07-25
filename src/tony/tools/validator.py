"""Argument validator."""

from __future__ import annotations

from tony.tools.models import (
    ToolArgument,
    ToolSelection,
    ValidationResult,
)


class ArgumentValidator:
    """Validates tool arguments."""

    def validate(
        self,
        selection: ToolSelection,
        arguments: list[ToolArgument],
    ) -> ValidationResult:
        """Validate tool arguments."""

        # TODO(M4): Use `selection` for tool-specific argument validation.
        _ = selection

        for argument in arguments:
            if not argument.name.strip():
                return ValidationResult(
                    valid=False,
                    reason="Argument name cannot be empty.",
                )

            if not argument.value.strip():
                return ValidationResult(
                    valid=False,
                    reason=f"Argument '{argument.name}' cannot be empty.",
                )

        return ValidationResult(
            valid=True,
            reason="Arguments are valid.",
        )
