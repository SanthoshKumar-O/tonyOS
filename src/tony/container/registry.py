from __future__ import annotations

from typing import Any


class ServiceAlreadyRegisteredError(RuntimeError):
    """Raised when attempting to register an existing service."""


class ServiceNotFoundError(RuntimeError):
    """Raised when requesting an unknown service."""


class ServiceRegistry:
    """Registry responsible for storing singleton services."""

    def __init__(self) -> None:
        self._services: dict[str, Any] = {}

    def register(self, name: str, service: Any) -> None:
        """Register a singleton service."""
        if name in self._services:
            raise ServiceAlreadyRegisteredError(f"Service '{name}' is already registered.")

        self._services[name] = service

    def resolve(self, name: str) -> Any:
        """Resolve a previously registered service."""
        try:
            return self._services[name]
        except KeyError as exc:
            raise ServiceNotFoundError(f"Service '{name}' is not registered.") from exc

    def has(self, name: str) -> bool:
        """Return True if a service exists."""
        return name in self._services
