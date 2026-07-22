"""Protocols for the LLM layer."""

from __future__ import annotations

from typing import Protocol


class LLMServiceProtocol(Protocol):
    """Language model interface."""

    def generate(self, prompt: str) -> str: ...
