"""Prompt loader."""

from __future__ import annotations

from pathlib import Path

from tony.prompts.exceptions import (
    PromptNotFoundError,
    PromptValidationError,
)
from tony.prompts.models import Prompt


class PromptLoader:
    """Loads prompt files from disk."""

    def __init__(self, prompt_directory: Path) -> None:
        self._prompt_directory = prompt_directory

    def load(self, name: str) -> Prompt:
        """Load a prompt by name."""

        path = self._prompt_directory / f"{name}.md"

        if not path.exists():
            raise PromptNotFoundError(f"Prompt '{name}' does not exist.")

        content = path.read_text(encoding="utf-8").strip()

        if not content:
            raise PromptValidationError(f"Prompt '{name}' is empty.")

        return Prompt(
            name=name,
            content=content,
        )
