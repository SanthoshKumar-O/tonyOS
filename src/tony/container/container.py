from __future__ import annotations

from logging import Logger

from tony.configuration import ConfigurationManager, TonyConfiguration
from tony.logging_system import get_logger
from tony.providers import ProviderManager

from .registry import ServiceRegistry


class TonyContainer:
    """Root dependency container for Tony."""

    def __init__(self) -> None:
        self._registry = ServiceRegistry()

    @property
    def configuration(self) -> TonyConfiguration:
        """Return the singleton configuration."""

        if not self._registry.has("configuration"):
            configuration = ConfigurationManager.load()
            self._registry.register("configuration", configuration)

        return self._registry.resolve("configuration")

    @property
    def logger(self) -> Logger:
        """Return the root application logger."""

        if not self._registry.has("logger"):
            logger = get_logger("tony")
            self._registry.register("logger", logger)

        return self._registry.resolve("logger")

    @property
    def providers(self) -> ProviderManager:
        if not self._registry.has("providers"):
            self._registry.register(
                "providers",
                ProviderManager(),
            )

        return self._registry.resolve("providers")
