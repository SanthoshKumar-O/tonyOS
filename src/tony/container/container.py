from __future__ import annotations

from logging import Logger

from tony.configuration import ConfigurationManager, TonyConfiguration
from tony.conversation.service import ConversationService
from tony.llm.service import LLMService
from tony.logging_system import get_logger
from tony.prompts import PromptBuilder, PromptManager
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

    @property
    def prompt_manager(self) -> PromptManager:
        if not self._registry.has("prompt_manager"):
            self._registry.register(
                "prompt_manager",
                PromptManager(),
            )

        return self._registry.resolve("prompt_manager")

    @property
    def prompt_builder(self) -> PromptBuilder:

        if not self._registry.has("prompt_builder"):
            self._registry.register(
                "prompt_builder",
                PromptBuilder(
                    self.prompt_manager,
                ),
            )

        return self._registry.resolve("prompt_builder")

    @property
    def llm_service(self) -> LLMService:

        if not self._registry.has("llm_service"):
            self._registry.register(
                "llm_service",
                LLMService(
                    self.providers,
                ),
            )

        return self._registry.resolve("llm_service")

    @property
    def conversation_service(self) -> ConversationService:

        if not self._registry.has("conversation_service"):
            self._registry.register(
                "conversation_service",
                ConversationService(
                    self.prompt_builder,
                    self.llm_service,
                ),
            )

        return self._registry.resolve("conversation_service")
