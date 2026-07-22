"""Prompt manager."""

from __future__ import annotations

from pathlib import Path

from tony.prompts.loader import PromptLoader
from tony.prompts.models import Prompt


class PromptManager:
    """Provides access to prompt documents."""

    def __init__(
        self,
        prompt_directory: Path = Path("data/prompts"),
    ) -> None:
        self._loader = PromptLoader(prompt_directory)

    def get(self, name: str) -> Prompt:
        """Return a prompt."""

        return self._loader.load(name)
