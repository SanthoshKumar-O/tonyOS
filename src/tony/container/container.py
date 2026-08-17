"""Tony dependency container."""

from __future__ import annotations

from logging import Logger

from tony.configuration import ConfigurationManager, TonyConfiguration
from tony.conversation.service import ConversationService
from tony.llm.service import LLMService
from tony.logging_system import get_logger
from tony.persistence import (
    PersistenceConfig,
    SQLitePersistence,
    SQLiteSessionRepository,
)
from tony.prompts import PromptBuilder, PromptManager
from tony.providers import ProviderManager
from tony.providers.ollama import OllamaProvider
from tony.session import SessionManager

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
    def persistence(self) -> SQLitePersistence:
        """Return the singleton initialized persistence backend."""

        if not self._registry.has("persistence"):
            persistence = SQLitePersistence(
                PersistenceConfig(
                    database_path=self.configuration.persistence.database_path,
                ),
            )
            persistence.initialize()
            self._registry.register("persistence", persistence)

        return self._registry.resolve("persistence")

    @property
    def session_repository(self) -> SQLiteSessionRepository:
        """Return the singleton session repository."""

        if not self._registry.has("session_repository"):
            self._registry.register(
                "session_repository",
                SQLiteSessionRepository(self.persistence),
            )

        return self._registry.resolve("session_repository")

    @property
    def session_manager(self) -> SessionManager:
        """Return the singleton session manager."""

        if not self._registry.has("session_manager"):
            self._registry.register(
                "session_manager",
                SessionManager(self.session_repository),
            )

        return self._registry.resolve("session_manager")

    @property
    def providers(self) -> ProviderManager:
        """Return the singleton provider manager."""

        if not self._registry.has("providers"):
            manager = ProviderManager()

            ollama = OllamaProvider(
                host=self.configuration.ollama.host,
                model=self.configuration.ollama.model,
                timeout=self.configuration.ollama.timeout,
            )

            manager.register(ollama)

            self._registry.register("providers", manager)

        return self._registry.resolve("providers")

    @property
    def prompt_manager(self) -> PromptManager:
        """Return the singleton prompt manager."""

        if not self._registry.has("prompt_manager"):
            self._registry.register(
                "prompt_manager",
                PromptManager(),
            )

        return self._registry.resolve("prompt_manager")

    @property
    def prompt_builder(self) -> PromptBuilder:
        """Return the singleton prompt builder."""

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
        """Return the singleton LLM service."""

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
        """Return the singleton conversation service."""

        if not self._registry.has("conversation_service"):
            self._registry.register(
                "conversation_service",
                ConversationService(
                    self.prompt_builder,
                    self.llm_service,
                ),
            )

        return self._registry.resolve("conversation_service")
