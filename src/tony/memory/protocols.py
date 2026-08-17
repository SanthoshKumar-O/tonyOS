"""Memory protocols."""

from __future__ import annotations

from typing import Protocol
from uuid import UUID

from tony.memory.models import Memory, MemoryDecision, MemoryScope


class MemoryStore(Protocol):
    """Protocol for memory storage."""

    def remember(self, memory: Memory) -> None:
        """Store a memory."""
        ...

    def recall(
        self,
        scope: MemoryScope | None = None,
    ) -> list[Memory]:
        """Return stored memories, optionally filtered by scope."""
        ...

    def forget(self, memory_id: UUID) -> None:
        """Remove a stored memory."""
        ...


class MemoryPolicy(Protocol):
    """Protocol for memory retention policy."""

    def evaluate(self, memory: Memory) -> MemoryDecision:
        """Evaluate whether a memory should be retained."""
        ...


class MemoryRetriever(Protocol):
    """Protocol for retrieving relevant memories."""

    def retrieve(
        self,
        query: str,
        scope: MemoryScope | None = None,
    ) -> list[Memory]:
        """Retrieve memories relevant to a query."""
        ...


class EmbeddingProvider(Protocol):
    """Protocol for converting text into vector representations."""

    def embed(self, text: str) -> list[float]:
        """Return an embedding for the supplied text."""
        ...
