from __future__ import annotations

from tony.context import (
    EnvironmentContext,
    ExecutionContextService,
    ExecutionSettings,
)
from tony.conversation import Conversation
from tony.memory import Memory, MemoryScope
from tony.session import Session


class DummyMemoryRetriever:
    def __init__(self, memories: list[Memory]) -> None:
        self._memories = memories
        self.queries: list[str] = []

    def retrieve(self, query: str, scope=None) -> list[Memory]:
        self.queries.append(query)

        return [
            memory
            for memory in self._memories
            if query.casefold() in memory.content.casefold()
        ]


def create_environment() -> EnvironmentContext:
    return EnvironmentContext(
        current_working_directory="/tmp",
        platform="Linux",
        hostname="fedora",
        python_version="3.14",
    )


def create_settings() -> ExecutionSettings:
    return ExecutionSettings(
        provider_name="ollama",
        temperature=0.0,
        streaming=False,
    )


def test_context_service_retrieves_memories_for_request() -> None:
    memory = Memory(
        content="Tony uses SQLite for persistence.",
        scope=MemoryScope.PROJECT,
    )

    retriever = DummyMemoryRetriever([memory])

    service = ExecutionContextService(
        memory_retriever=retriever,
    )

    context = service.create(
        session=Session(),
        conversation=Conversation(),
        user_input="SQLite",
        environment=create_environment(),
        settings=create_settings(),
    )

    assert context.retrieved_memories == (memory,)
    assert retriever.queries == ["SQLite"]


def test_context_service_without_retriever_has_no_retrieved_memories() -> None:
    service = ExecutionContextService()

    context = service.create(
        session=Session(),
        conversation=Conversation(),
        user_input="SQLite",
        environment=create_environment(),
        settings=create_settings(),
    )

    assert context.retrieved_memories == ()
