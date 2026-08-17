from __future__ import annotations

from tony.memory import Memory, MemoryScope, SQLiteMemoryStore
from tony.persistence import PersistenceConfig, SQLitePersistence


def create_store(tmp_path):
    persistence = SQLitePersistence(
        PersistenceConfig(
            database_path=tmp_path / "tony.db",
        ),
    )
    persistence.initialize()

    return persistence, SQLiteMemoryStore(persistence)


def test_remember_and_recall(tmp_path) -> None:
    persistence, store = create_store(tmp_path)

    memory = Memory(
        content="Tony is local-first.",
        scope=MemoryScope.PROJECT,
    )

    store.remember(memory)

    assert store.recall() == [memory]

    persistence.close()


def test_recall_filters_by_scope(tmp_path) -> None:
    persistence, store = create_store(tmp_path)

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

    assert store.recall(MemoryScope.PROJECT) == [project]
    assert store.recall(MemoryScope.WORKSPACE) == [workspace]

    persistence.close()


def test_forget(tmp_path) -> None:
    persistence, store = create_store(tmp_path)

    memory = Memory(
        content="Temporary memory.",
        scope=MemoryScope.WORKING,
    )

    store.remember(memory)
    store.forget(memory.id)

    assert store.recall() == []

    persistence.close()


def test_forget_unknown_id_is_safe(tmp_path) -> None:
    persistence, store = create_store(tmp_path)

    from uuid import uuid4

    store.forget(uuid4())

    assert store.recall() == []

    persistence.close()


def test_memory_survives_persistence_restart(tmp_path) -> None:
    memory = Memory(
        content="Tony memories survive application restart.",
        scope=MemoryScope.PROJECT,
    )

    persistence_a, store_a = create_store(tmp_path)
    store_a.remember(memory)
    persistence_a.close()

    persistence_b, store_b = create_store(tmp_path)

    restored = store_b.recall()

    assert restored == [memory]

    persistence_b.close()


def test_remember_updates_existing_memory(tmp_path) -> None:
    persistence, store = create_store(tmp_path)

    memory = Memory(
        content="Original memory.",
        scope=MemoryScope.PROJECT,
    )

    store.remember(memory)

    updated = memory.model_copy(
        update={
            "content": "Updated memory.",
        },
    )

    store.remember(updated)

    restored = store.recall()

    assert restored == [updated]
    assert len(restored) == 1

    persistence.close()


class DummyEmbeddingProvider:
    """Deterministic embedding provider for SQLite store tests."""

    def embed(self, text: str) -> list[float]:
        return [float(len(text)), 1.0, 2.0]


def create_store_with_embeddings(tmp_path):
    persistence = SQLitePersistence(
        PersistenceConfig(
            database_path=tmp_path / "tony.db",
        ),
    )
    persistence.initialize()

    return persistence, SQLiteMemoryStore(
        persistence,
        embedding_provider=DummyEmbeddingProvider(),
    )


def test_remember_persists_embedding(tmp_path) -> None:
    persistence, store = create_store_with_embeddings(tmp_path)

    memory = Memory(
        content="Tony is local-first.",
        scope=MemoryScope.PROJECT,
    )

    store.remember(memory)

    row = persistence.connection.execute(
        """
        SELECT embedding
        FROM memory_embeddings
        WHERE memory_id = ?
        """,
        (str(memory.id),),
    ).fetchone()

    assert row is not None
    assert row[0] == '[20.0, 1.0, 2.0]'

    persistence.close()


def test_remember_updates_existing_embedding(tmp_path) -> None:
    persistence, store = create_store_with_embeddings(tmp_path)

    memory = Memory(
        content="Original",
        scope=MemoryScope.PROJECT,
    )

    store.remember(memory)

    updated = memory.model_copy(
        update={
            "content": "Updated memory",
        },
    )

    store.remember(updated)

    row = persistence.connection.execute(
        """
        SELECT embedding
        FROM memory_embeddings
        WHERE memory_id = ?
        """,
        (str(memory.id),),
    ).fetchone()

    assert row is not None
    assert row[0] == '[14.0, 1.0, 2.0]'

    persistence.close()


def test_embedding_survives_persistence_restart(tmp_path) -> None:
    memory = Memory(
        content="Tony remembers this.",
        scope=MemoryScope.PROJECT,
    )

    persistence_a, store_a = create_store_with_embeddings(tmp_path)
    store_a.remember(memory)
    persistence_a.close()

    persistence_b, _ = create_store_with_embeddings(tmp_path)

    row = persistence_b.connection.execute(
        """
        SELECT embedding
        FROM memory_embeddings
        WHERE memory_id = ?
        """,
        (str(memory.id),),
    ).fetchone()

    assert row is not None
    assert row[0] == '[20.0, 1.0, 2.0]'

    persistence_b.close()


def test_forget_removes_embedding(tmp_path) -> None:
    persistence, store = create_store_with_embeddings(tmp_path)

    memory = Memory(
        content="Temporary semantic memory.",
        scope=MemoryScope.WORKING,
    )

    store.remember(memory)
    store.forget(memory.id)

    row = persistence.connection.execute(
        """
        SELECT embedding
        FROM memory_embeddings
        WHERE memory_id = ?
        """,
        (str(memory.id),),
    ).fetchone()

    assert row is None

    persistence.close()
