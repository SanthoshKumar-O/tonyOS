"""Protocols for the prompt system."""

from __future__ import annotations

from typing import Protocol

from tony.conversation import Conversation
from tony.prompts.models import Prompt


class PromptManagerProtocol(Protocol):
    """Provides prompt documents."""

    def get(self, name: str) -> Prompt: ...


class PromptBuilderProtocol(Protocol):
    """Builds prompts for the LLM."""

    def build(self, conversation: Conversation) -> str: ...
