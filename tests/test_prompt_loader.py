from __future__ import annotations

from pathlib import Path

import pytest

from tony.prompts.exceptions import (
    PromptNotFoundError,
    PromptValidationError,
)
from tony.prompts.loader import PromptLoader


def test_load_existing_prompt(tmp_path: Path) -> None:
    prompt_dir = tmp_path / "prompts"
    prompt_dir.mkdir()

    (prompt_dir / "system.md").write_text(
        "Hello Tony",
        encoding="utf-8",
    )

    loader = PromptLoader(prompt_dir)

    prompt = loader.load("system")

    assert prompt.name == "system"
    assert prompt.content == "Hello Tony"


def test_missing_prompt(tmp_path: Path) -> None:
    prompt_dir = tmp_path / "prompts"
    prompt_dir.mkdir()

    loader = PromptLoader(prompt_dir)

    with pytest.raises(PromptNotFoundError):
        loader.load("missing")


def test_empty_prompt(tmp_path: Path) -> None:
    prompt_dir = tmp_path / "prompts"
    prompt_dir.mkdir()

    (prompt_dir / "empty.md").write_text(
        "",
        encoding="utf-8",
    )

    loader = PromptLoader(prompt_dir)

    with pytest.raises(PromptValidationError):
        loader.load("empty")
