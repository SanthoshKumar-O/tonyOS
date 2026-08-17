from __future__ import annotations

from uuid import UUID

from tony.memory import Memory, MemoryManager, MemoryScope


class DummyMemoryStore:
    """In-memory store for manager tests."""

    def __init__(self) -> None:
        self.memories: dict[UUID, Memory] = {}

    def remember(self, memory: Memory) -> None:
        self.memories[memory.id] = memory

    def recall(
        self,
        scope: MemoryScope | None = None,
    ) -> list[Memory]:
        memories = list(self.memories.values())

        if scope is None:
            return memories

        return [
            memory
            for memory in memories
            if memory.scope is scope
        ]

    def forget(self, memory_id: UUID) -> None:
        self.memories.pop(memory_id, None)


def test_remember() -> None:
    store = DummyMemoryStore()
    manager = MemoryManager(store)

    memory = Memory(
        content="Tony is local-first.",
        scope=MemoryScope.PROJECT,
    )

    manager.remember(memory)

    assert store.memories[memory.id] == memory


def test_recall() -> None:
    store = DummyMemoryStore()
    manager = MemoryManager(store)

    memory = Memory(
        content="Tony runs on Fedora.",
        scope=MemoryScope.WORKSPACE,
    )

    store.remember(memory)

    assert manager.recall() == [memory]


def test_recall_by_scope() -> None:
    store = DummyMemoryStore()
    manager = MemoryManager(store)

    project = Memory(
        content="Tony uses SQLite.",
        scope=MemoryScope.PROJECT,
    )

    workspace = Memory(
        content="Tony runs on Fedora.",
        scope=MemoryScope.WORKSPACE,
    )

    store.remember(project)
    store.remember(workspace)

    assert manager.recall(MemoryScope.PROJECT) == [project]


def test_forget() -> None:
    store = DummyMemoryStore()
    manager = MemoryManager(store)

    memory = Memory(
        content="Temporary memory.",
        scope=MemoryScope.WORKING,
    )

    manager.remember(memory)
    manager.forget(memory.id)

    assert manager.recall() == []


class DenyingMemoryPolicy:
    """Policy used to verify manager rejection."""

    def evaluate(self, memory: Memory):
        from tony.memory import MemoryDecision

        return MemoryDecision(
            allowed=False,
            reason="Memory rejected by policy.",
        )


def test_remember_uses_policy() -> None:
    store = DummyMemoryStore()
    manager = MemoryManager(
        store,
        policy=DenyingMemoryPolicy(),
    )

    memory = Memory(
        content="Rejected memory.",
        scope=MemoryScope.PROJECT,
    )

    manager.remember(memory)

    assert store.memories == {}
