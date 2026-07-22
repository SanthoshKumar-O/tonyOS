from __future__ import annotations

from abc import ABC, abstractmethod


class Provider(ABC):
    """Base class for all Tony providers."""

    def __init__(self, name: str) -> None:
        self._name = name
        self._initialized = False

    @property
    def name(self) -> str:
        """Return the provider name."""
        return self._name

    @property
    def initialized(self) -> bool:
        """Return whether the provider has been initialized."""
        return self._initialized

    @abstractmethod
    def initialize(self) -> None:
        """Initialize the provider."""

    @abstractmethod
    def shutdown(self) -> None:
        """Shutdown the provider."""

    def _mark_initialized(self) -> None:
        self._initialized = True

    def _mark_shutdown(self) -> None:
        self._initialized = False

    @abstractmethod
    def generate(self, prompt: str) -> str:
        """Generate text from the given prompt."""
