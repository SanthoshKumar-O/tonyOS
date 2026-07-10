from __future__ import annotations

from .base import Provider
from .exceptions import (
    ProviderAlreadyRegisteredError,
    ProviderNotFoundError,
)


class ProviderManager:
    """Manages all registered providers."""

    def __init__(self) -> None:
        self._providers: dict[str, Provider] = {}

    def register(self, provider: Provider) -> None:
        """Register a provider."""

        if provider.name in self._providers:
            raise ProviderAlreadyRegisteredError(
                f"Provider '{provider.name}' is already registered."
            )

        self._providers[provider.name] = provider

    def unregister(self, name: str) -> None:
        """Remove a provider."""

        if name not in self._providers:
            raise ProviderNotFoundError(f"Provider '{name}' is not registered.")

        del self._providers[name]

    def get(self, name: str) -> Provider:
        """Return a registered provider."""

        try:
            return self._providers[name]
        except KeyError as exc:
            raise ProviderNotFoundError(f"Provider '{name}' is not registered.") from exc

    def has(self, name: str) -> bool:
        """Return True if a provider exists."""

        return name in self._providers

    def list(self) -> list[str]:
        """Return provider names."""

        return sorted(self._providers.keys())
