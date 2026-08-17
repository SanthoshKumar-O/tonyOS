"""Memory manager."""

from __future__ import annotations

from uuid import UUID

from tony.memory.models import Memory, MemoryScope
from tony.memory.policy import DefaultMemoryPolicy
from tony.memory.protocols import MemoryPolicy, MemoryStore


class MemoryManager:
    """Manages Tony's memories."""

    def __init__(
        self,
        store: MemoryStore,
        policy: MemoryPolicy | None = None,
    ) -> None:
        """Create the memory manager."""
        self._store = store
        self._policy = policy or DefaultMemoryPolicy()

    def remember(self, memory: Memory) -> None:
        """Store a memory if permitted by the policy."""
        decision = self._policy.evaluate(memory)

        if not decision.allowed:
            return

        self._store.remember(memory)

    def recall(
        self,
        scope: MemoryScope | None = None,
    ) -> list[Memory]:
        """Return memories, optionally filtered by scope."""
        return self._store.recall(scope)

    def forget(self, memory_id: UUID) -> None:
        """Forget a memory."""
        self._store.forget(memory_id)
