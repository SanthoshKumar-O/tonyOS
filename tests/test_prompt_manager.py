from __future__ import annotations

from tony.prompts import PromptManager


def test_get_prompt(tmp_path) -> None:
    prompt_dir = tmp_path / "prompts"
    prompt_dir.mkdir()

    (prompt_dir / "system.md").write_text(
        "You are Tony.",
        encoding="utf-8",
    )

    manager = PromptManager(prompt_dir)

    prompt = manager.get("system")

    assert prompt.name == "system"
    assert prompt.content == "You are Tony."
