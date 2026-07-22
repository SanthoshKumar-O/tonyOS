"""Prompt builder."""

from __future__ import annotations

from tony.conversation import Conversation
from tony.prompts.protocols import PromptManagerProtocol


class PromptBuilder:
    """Builds prompts for the language model."""

    def __init__(
        self,
        prompt_manager: PromptManagerProtocol,
    ) -> None:
        self._prompt_manager = prompt_manager

    def build(
        self,
        conversation: Conversation,
    ) -> str:
        """Build a prompt string."""
        system_prompt = self._prompt_manager.get("system")
        parts: list[str] = []
        parts.append(system_prompt.content.strip())
        parts.append("")

        for message in conversation.messages:
            parts.append(f"{message.role.value}:")
            parts.append(message.content)
            parts.append("")

        return "\n".join(parts).strip()
