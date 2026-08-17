"""SQLite memory store implementation."""

from __future__ import annotations

import json
from datetime import datetime
from uuid import UUID

from tony.memory.models import Memory, MemoryScope
from tony.memory.protocols import EmbeddingProvider, MemoryStore
from tony.persistence.sqlite import SQLitePersistence


class SQLiteMemoryStore(MemoryStore):
    """Persists Tony memories using SQLite."""

    def __init__(
        self,
        persistence: SQLitePersistence,
        embedding_provider: EmbeddingProvider | None = None,
    ) -> None:
        self._persistence = persistence
        self._embedding_provider = embedding_provider

    @property
    def _connection(self):
        """Return the active persistence connection."""

        return self._persistence.connection

    def remember(self, memory: Memory) -> None:
        """Persist a memory."""

        self._connection.execute(
            """
            INSERT INTO memories (
                id,
                content,
                scope,
                created_at
            )
            VALUES (?, ?, ?, ?)
            ON CONFLICT(id) DO UPDATE SET
                content = excluded.content,
                scope = excluded.scope,
                created_at = excluded.created_at
            """,
            (
                str(memory.id),
                memory.content,
                memory.scope.value,
                memory.created_at.isoformat(),
            ),
        )

        if self._embedding_provider is not None:
            embedding = self._embedding_provider.embed(memory.content)

            self._connection.execute(
                """
                INSERT INTO memory_embeddings (
                    memory_id,
                    embedding
                )
                VALUES (?, ?)
                ON CONFLICT(memory_id) DO UPDATE SET
                    embedding = excluded.embedding
                """,
                (
                    str(memory.id),
                    json.dumps(embedding),
                ),
            )

        self._connection.commit()

    def recall(
        self,
        scope: MemoryScope | None = None,
    ) -> list[Memory]:
        """Return persisted memories, optionally filtered by scope."""

        if scope is None:
            rows = self._connection.execute(
                """
                SELECT
                    id,
                    content,
                    scope,
                    created_at
                FROM memories
                ORDER BY created_at, id
                """
            ).fetchall()
        else:
            rows = self._connection.execute(
                """
                SELECT
                    id,
                    content,
                    scope,
                    created_at
                FROM memories
                WHERE scope = ?
                ORDER BY created_at, id
                """,
                (scope.value,),
            ).fetchall()

        return [
            Memory(
                id=UUID(row[0]),
                content=row[1],
                scope=MemoryScope(row[2]),
                created_at=datetime.fromisoformat(row[3]),
            )
            for row in rows
        ]

    def forget(self, memory_id: UUID) -> None:
        """Remove a persisted memory."""

        self._connection.execute(
            """
            DELETE FROM memories
            WHERE id = ?
            """,
            (str(memory_id),),
        )

        self._connection.commit()
