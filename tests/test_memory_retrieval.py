from __future__ import annotations

from tony.memory import Memory, MemoryRetriever, MemoryScope


class DummyMemoryRetriever:
    """In-memory implementation used to verify the retrieval contract."""

    def __init__(self, memories: list[Memory]) -> None:
        self._memories = memories

    def retrieve(
        self,
        query: str,
        scope: MemoryScope | None = None,
    ) -> list[Memory]:
        memories = self._memories

        if scope is not None:
            memories = [
                memory
                for memory in memories
                if memory.scope is scope
            ]

        return [
            memory
            for memory in memories
            if query.lower() in memory.content.lower()
        ]


def test_memory_retriever_protocol() -> None:
    memory = Memory(
        content="Tony uses SQLite for persistence.",
        scope=MemoryScope.PROJECT,
    )

    retriever: MemoryRetriever = DummyMemoryRetriever([memory])

    result = retriever.retrieve("SQLite")

    assert result == [memory]


def test_memory_retriever_supports_scope_filter() -> None:
    project_memory = Memory(
        content="Tony uses SQLite.",
        scope=MemoryScope.PROJECT,
    )

    workspace_memory = Memory(
        content="Tony runs on Fedora.",
        scope=MemoryScope.WORKSPACE,
    )

    retriever: MemoryRetriever = DummyMemoryRetriever(
        [project_memory, workspace_memory]
    )

    result = retriever.retrieve(
        "Tony",
        scope=MemoryScope.PROJECT,
    )

    assert result == [project_memory]


def test_memory_retriever_returns_empty_when_not_relevant() -> None:
    memory = Memory(
        content="Tony uses SQLite.",
        scope=MemoryScope.PROJECT,
    )

    retriever: MemoryRetriever = DummyMemoryRetriever([memory])

    assert retriever.retrieve("Fedora") == []


class DummyMemoryStore:
    """In-memory store for deterministic retrieval tests."""

    def __init__(self, memories: list[Memory]) -> None:
        self._memories = memories

    def remember(self, memory: Memory) -> None:
        self._memories.append(memory)

    def recall(
        self,
        scope: MemoryScope | None = None,
    ) -> list[Memory]:
        if scope is None:
            return list(self._memories)

        return [
            memory
            for memory in self._memories
            if memory.scope is scope
        ]

    def forget(self, memory_id) -> None:
        self._memories = [
            memory
            for memory in self._memories
            if memory.id != memory_id
        ]


def test_default_memory_retriever_matches_content() -> None:
    from tony.memory import DefaultMemoryRetriever

    memory = Memory(
        content="Tony uses SQLite for persistence.",
        scope=MemoryScope.PROJECT,
    )

    retriever = DefaultMemoryRetriever(
        DummyMemoryStore([memory])
    )

    assert retriever.retrieve("SQLite") == [memory]


def test_default_memory_retriever_is_case_insensitive() -> None:
    from tony.memory import DefaultMemoryRetriever

    memory = Memory(
        content="Tony runs on Fedora.",
        scope=MemoryScope.WORKSPACE,
    )

    retriever = DefaultMemoryRetriever(
        DummyMemoryStore([memory])
    )

    assert retriever.retrieve("FEDORA") == [memory]


def test_default_memory_retriever_supports_scope_filter() -> None:
    from tony.memory import DefaultMemoryRetriever

    project_memory = Memory(
        content="Tony uses SQLite.",
        scope=MemoryScope.PROJECT,
    )

    workspace_memory = Memory(
        content="Tony runs on Fedora.",
        scope=MemoryScope.WORKSPACE,
    )

    retriever = DefaultMemoryRetriever(
        DummyMemoryStore(
            [project_memory, workspace_memory]
        )
    )

    assert retriever.retrieve(
        "Tony",
        scope=MemoryScope.PROJECT,
    ) == [project_memory]


def test_default_memory_retriever_returns_empty_when_not_relevant() -> None:
    from tony.memory import DefaultMemoryRetriever

    memory = Memory(
        content="Tony uses SQLite.",
        scope=MemoryScope.PROJECT,
    )

    retriever = DefaultMemoryRetriever(
        DummyMemoryStore([memory])
    )

    assert retriever.retrieve("Fedora") == []


def test_default_memory_retriever_rejects_empty_query() -> None:
    from tony.memory import DefaultMemoryRetriever

    memory = Memory(
        content="Tony uses SQLite.",
        scope=MemoryScope.PROJECT,
    )

    retriever = DefaultMemoryRetriever(
        DummyMemoryStore([memory])
    )

    assert retriever.retrieve("") == []
    assert retriever.retrieve("   ") == []
