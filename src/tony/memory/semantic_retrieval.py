"""Semantic memory retrieval using persisted embeddings."""

from __future__ import annotations

import json
import math

from tony.memory.models import Memory, MemoryScope
from tony.memory.protocols import EmbeddingProvider
from tony.persistence.sqlite import SQLitePersistence


class SemanticMemoryRetriever:
    """Retrieves memories using cosine similarity between embeddings."""

    def __init__(
        self,
        persistence: SQLitePersistence,
        embedding_provider: EmbeddingProvider,
        min_similarity: float = 0.0,
    ) -> None:
        """Create a semantic retriever."""
        if not 0.0 <= min_similarity <= 1.0:
            raise ValueError("min_similarity must be between 0.0 and 1.0")

        self._persistence = persistence
        self._embedding_provider = embedding_provider
        self._min_similarity = min_similarity

    @property
    def _connection(self):
        """Return the active persistence connection."""
        return self._persistence.connection

    @staticmethod
    def _cosine_similarity(
        first: list[float],
        second: list[float],
    ) -> float:
        """Calculate cosine similarity between two vectors."""
        if len(first) != len(second):
            return 0.0

        first_norm = math.sqrt(sum(value * value for value in first))
        second_norm = math.sqrt(sum(value * value for value in second))

        if first_norm == 0.0 or second_norm == 0.0:
            return 0.0

        dot_product = sum(
            left * right
            for left, right in zip(first, second)
        )

        return dot_product / (first_norm * second_norm)

    def retrieve(
        self,
        query: str,
        scope: MemoryScope | None = None,
    ) -> list[Memory]:
        """Return memories ranked by semantic similarity."""
        if not query.strip():
            return []

        query_embedding = self._embedding_provider.embed(query)

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

        results: list[tuple[float, Memory]] = []

        for row in rows:
            memory = Memory(
                id=row[0],
                content=row[1],
                scope=MemoryScope(row[2]),
                created_at=row[3],
            )

            embedding = json.loads(row[4])
            similarity = self._cosine_similarity(
                query_embedding,
                embedding,
            )

            if similarity >= self._min_similarity:
                results.append((similarity, memory))

        results.sort(
            key=lambda item: (-item[0], str(item[1].id)),
        )

        return [memory for _, memory in results]
