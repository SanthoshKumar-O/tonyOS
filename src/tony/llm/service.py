"""LLM service abstraction."""

from __future__ import annotations

from tony.llm.exceptions import (
    LLMGenerationError,
    LLMInitializationError,
)
from tony.providers.base import Provider
from tony.providers.manager import ProviderManager


class LLMService:
    """High-level interface for text generation."""

    def __init__(self, provider_manager: ProviderManager) -> None:
        """Create the LLM service."""
        self._provider_manager = provider_manager
        self._provider: Provider | None = None

    @property
    def initialized(self) -> bool:
        """Whether the service has been initialized."""
        return self._provider is not None

    def initialize(self) -> None:
        """Initialize the LLM service."""

        provider = self._provider_manager.get("ollama")

        if provider is None:
            raise LLMInitializationError("No provider named 'ollama' is registered.")

        if not provider.initialized:
            raise LLMInitializationError("Provider has not been initialized.")

        self._provider = provider

    def generate(self, prompt: str) -> str:
        """Generate text."""

        if self._provider is None:
            raise LLMInitializationError("LLMService has not been initialized.")

        try:
            return self._provider.generate(prompt)

        except Exception as exc:
            raise LLMGenerationError("Text generation failed.") from exc
