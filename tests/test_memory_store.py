from __future__ import annotations

from uuid import UUID, uuid4

from tony.memory import Memory, MemoryScope, MemoryStore


class DummyMemoryStore:
    """In-memory implementation used to verify the MemoryStore contract."""

    def __init__(self) -> None:
        self._memories: dict[UUID, Memory] = {}

    def remember(self, memory: Memory) -> None:
        self._memories[memory.id] = memory

    def recall(
        self,
        scope: MemoryScope | None = None,
    ) -> list[Memory]:
        memories = list(self._memories.values())

        if scope is None:
            return memories

        return [memory for memory in memories if memory.scope is scope]

    def forget(self, memory_id: UUID) -> None:
        self._memories.pop(memory_id, None)


def test_memory_store_protocol() -> None:
    store: MemoryStore = DummyMemoryStore()

    memory = Memory(
        content="Tony is local-first.",
        scope=MemoryScope.PROJECT,
    )

    store.remember(memory)

    result = store.recall()

    assert result == [memory]


def test_memory_store_recall_filters_by_scope() -> None:
    store: MemoryStore = DummyMemoryStore()

    project_memory = Memory(
        content="Tony uses SQLite.",
        scope=MemoryScope.PROJECT,
    )

    workspace_memory = Memory(
        content="Tony runs on Fedora.",
        scope=MemoryScope.WORKSPACE,
    )

    store.remember(project_memory)
    store.remember(workspace_memory)

    result = store.recall(MemoryScope.PROJECT)

    assert result == [project_memory]


def test_memory_store_forget() -> None:
    store: MemoryStore = DummyMemoryStore()

    memory = Memory(
        content="Temporary working memory.",
        scope=MemoryScope.WORKING,
    )

    store.remember(memory)
    store.forget(memory.id)

    assert store.recall() == []


def test_memory_store_forget_unknown_id() -> None:
    store: MemoryStore = DummyMemoryStore()

    store.forget(uuid4())

    assert store.recall() == []
