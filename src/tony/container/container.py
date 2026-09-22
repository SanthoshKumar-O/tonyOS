"""Tony dependency container."""

from __future__ import annotations

from logging import Logger

from tony.clarification import ClarificationEngine
from tony.configuration import ConfigurationManager, TonyConfiguration
from tony.context_builder import ContextBuilder
from tony.conversation.service import ConversationService
from tony.llm.service import LLMService
from tony.logging_system import get_logger
from tony.memory import (
    DefaultMemoryRetriever,
    MemoryManager,
    OllamaEmbeddingProvider,
    SQLiteMemoryStore,
)
from tony.context import ExecutionContextService
from tony.persistence import (
    PersistenceConfig,
    SQLitePersistence,
    SQLiteSessionRepository,
)
from tony.pipeline import IntelligencePipeline
from tony.planner import (
    IntentClassifier,
    PlanFactory,
    PlannerService,
)
from tony.planner.selector import ToolSelector
from tony.prompts import PromptBuilder, PromptManager
from tony.providers import ProviderManager
from tony.providers.ollama import OllamaProvider
from tony.response import ResponseGenerator
from tony.session import SessionManager
from tony.streaming import ResponseStreamer
from tony.tools import ToolRegistry
from tony.tools.archive import register_archive_tools
from tony.tools.docker import DockerRegistry
from tony.tools.filesystem.registry import register_filesystem_tools
from tony.tools.git import GitRegistry
from tony.tools.media import register_media_tools
from tony.tools.package import PackageRegistry
from tony.tools.process import register_process_tools
from tony.tools.python import PythonRegistry
from tony.tools.search import register_search_tools
from tony.tools.systemctl import SystemctlRegistry
from tony.tools.terminal import TerminalRegistry
from tony.tools.workspace import register_workspace_tools

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
    def tool_registry(self) -> ToolRegistry:
        """Return the singleton tool registry."""

        if not self._registry.has("tool_registry"):
            registry = ToolRegistry()

            register_filesystem_tools(registry)
            GitRegistry.register(registry)
            TerminalRegistry.register(registry)
            register_process_tools(registry)
            PackageRegistry.register(registry)
            PythonRegistry.register(registry)
            DockerRegistry.register(registry)
            SystemctlRegistry.register(registry)
            register_archive_tools(registry)
            register_media_tools(registry)
            register_search_tools(registry)
            register_workspace_tools(registry)

            self._registry.register(
                "tool_registry",
                registry,
            )

        return self._registry.resolve("tool_registry")

    @property
    def memory_store(self) -> SQLiteMemoryStore:
        """Return the singleton memory store."""

        if not self._registry.has("memory_store"):
            self._registry.register(
                "memory_store",
                SQLiteMemoryStore(
                    self.persistence,
                    embedding_provider=OllamaEmbeddingProvider(
                        self.providers.get("ollama"),
                    ),
                ),
            )

        return self._registry.resolve("memory_store")

    @property
    def memory_manager(self) -> MemoryManager:
        """Return the singleton memory manager."""

        if not self._registry.has("memory_manager"):
            self._registry.register(
                "memory_manager",
                MemoryManager(self.memory_store),
            )

        return self._registry.resolve("memory_manager")
    
    @property
    def memory_retriever(self) -> DefaultMemoryRetriever:
        """Return the singleton memory retriever."""

        if not self._registry.has("memory_retriever"):
            self._registry.register(
                "memory_retriever",
                DefaultMemoryRetriever(self.memory_store),
            )

        return self._registry.resolve("memory_retriever")

    @property
    def context_service(self) -> ExecutionContextService:
        """Return the singleton execution context service."""

        if not self._registry.has("context_service"):
            self._registry.register(
                "context_service",
                ExecutionContextService(
                    memory_retriever=self.memory_retriever,
                ),
            )

        return self._registry.resolve("context_service")

    @property
    def providers(self) -> ProviderManager:
        """Return the singleton provider manager."""

        if not self._registry.has("providers"):
            manager = ProviderManager()

            ollama = OllamaProvider(
                host=self.configuration.ollama.host,
                model=self.configuration.ollama.model,
                embedding_model=self.configuration.ollama.embedding_model,
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

    @property
    def intelligence_pipeline(self) -> IntelligencePipeline:
        """Return the singleton intelligence pipeline."""

        if not self._registry.has("intelligence_pipeline"):
            self._registry.register(
                "intelligence_pipeline",
                IntelligencePipeline(
                    context_builder=ContextBuilder(
                        prompt_manager=self.prompt_manager,
                        prompt_builder=self.prompt_builder,
                    ),
                    planner=PlannerService(
    classifier=IntentClassifier(),
    factory=PlanFactory(),
    selector=ToolSelector(self.tool_registry),
),
                    clarification_engine=ClarificationEngine(),
                    response_generator=ResponseGenerator(),
                    response_streamer=ResponseStreamer(),
                ),
            )

        return self._registry.resolve("intelligence_pipeline")
