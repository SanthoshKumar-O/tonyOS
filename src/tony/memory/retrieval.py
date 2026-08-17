"""Memory retrieval implementations."""

from __future__ import annotations

import json
import math
from datetime import datetime
from uuid import UUID

from tony.memory.models import Memory, MemoryScope
from tony.memory.protocols import EmbeddingProvider, MemoryRetriever, MemoryStore
from tony.persistence.sqlite import SQLitePersistence


class DefaultMemoryRetriever(MemoryRetriever):
    """Retrieves memories using deterministic text matching."""

    def __init__(self, store: MemoryStore) -> None:
        """Create a retriever backed by a memory store."""
        self._store = store

    def retrieve(
        self,
        query: str,
        scope: MemoryScope | None = None,
    ) -> list[Memory]:
        """Return memories whose content contains the query."""
        normalized_query = query.strip().casefold()

        if not normalized_query:
            return []

        memories = self._store.recall(scope)

        return [
            memory
            for memory in memories
            if normalized_query in memory.content.casefold()
        ]


class SemanticMemoryRetriever(MemoryRetriever):
    """Retrieves memories using embedding cosine similarity."""

    def __init__(
        self,
        persistence: SQLitePersistence,
        embedding_provider: EmbeddingProvider,
        min_similarity: float = 0.5,
    ) -> None:
        """Create a semantic retriever."""
        self._persistence = persistence
        self._embedding_provider = embedding_provider
        self._min_similarity = min_similarity

    @property
    def _connection(self):
        """Return the active persistence connection."""
        return self._persistence.connection

    @staticmethod
    def _cosine_similarity(
        left: list[float],
        right: list[float],
    ) -> float:
        """Calculate cosine similarity between two vectors."""
        if len(left) != len(right):
            return 0.0

        left_norm = math.sqrt(sum(value * value for value in left))
        right_norm = math.sqrt(sum(value * value for value in right))

        if left_norm == 0.0 or right_norm == 0.0:
            return 0.0

        dot_product = sum(
            left_value * right_value
            for left_value, right_value in zip(left, right)
        )

        return dot_product / (left_norm * right_norm)

    def retrieve(
        self,
        query: str,
        scope: MemoryScope | None = None,
    ) -> list[Memory]:
        """Return memories ranked by semantic similarity."""
        if not query.strip():
            return []

        query_embedding = self._embedding_provider.embed(query.strip())

        if scope is None:
            rows = self._connection.execute(
                """
                SELECT
                    m.id,
                    m.content,
                    m.scope,
                    m.created_at,
                    e.embedding
                FROM memories AS m
                INNER JOIN memory_embeddings AS e
                    ON e.memory_id = m.id
                """
            ).fetchall()
        else:
            rows = self._connection.execute(
                """
                SELECT
                    m.id,
                    m.content,
                    m.scope,
                    m.created_at,
                    e.embedding
                FROM memories AS m
                INNER JOIN memory_embeddings AS e
                    ON e.memory_id = m.id
                WHERE m.scope = ?
                """,
                (scope.value,),
            ).fetchall()

        ranked: list[tuple[float, Memory]] = []

        for row in rows:
            embedding = json.loads(row[4])

            similarity = self._cosine_similarity(
                query_embedding,
                embedding,
            )

            if similarity < self._min_similarity:
                continue

            memory = Memory(
                id=UUID(row[0]),
                content=row[1],
                scope=MemoryScope(row[2]),
                created_at=datetime.fromisoformat(row[3]),
            )

            ranked.append((similarity, memory))

        ranked.sort(
            key=lambda item: (
                -item[0],
                item[1].created_at,
                str(item[1].id),
            )
        )

        return [memory for _, memory in ranked]
