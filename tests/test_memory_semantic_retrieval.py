from __future__ import annotations

from tony.memory import (
    Memory,
    MemoryScope,
    SemanticMemoryRetriever,
    SQLiteMemoryStore,
)
from tony.persistence import PersistenceConfig, SQLitePersistence


class DummyEmbeddingProvider:
    """Deterministic embedding provider for semantic retrieval tests."""

    def embed(self, text: str) -> list[float]:
        values = {
            "database": [1.0, 0.0],
            "storage": [0.9, 0.1],
            "fedora": [0.0, 1.0],
            "unrelated": [-1.0, 0.0],
            "tony uses sqlite.": [1.0, 0.0],
            "tony stores persistent data.": [0.9, 0.1],
            "tony runs on fedora.": [0.0, 1.0],
        }

        return values.get(text.casefold(), [0.0, 0.0])


def create_retriever(tmp_path):
    persistence = SQLitePersistence(
        PersistenceConfig(
            database_path=tmp_path / "tony.db",
        ),
    )
    persistence.initialize()

    provider = DummyEmbeddingProvider()
    store = SQLiteMemoryStore(
        persistence,
        embedding_provider=provider,
    )

    return (
        persistence,
        store,
        SemanticMemoryRetriever(
            persistence,
            provider,
            min_similarity=0.5,
        ),
    )


def test_semantic_retrieval_ranks_by_similarity(tmp_path) -> None:
    persistence, store, retriever = create_retriever(tmp_path)

    database = Memory(
        content="Tony uses SQLite.",
        scope=MemoryScope.PROJECT,
    )
    storage = Memory(
        content="Tony stores persistent data.",
        scope=MemoryScope.PROJECT,
    )
    fedora = Memory(
        content="Tony runs on Fedora.",
        scope=MemoryScope.WORKSPACE,
    )

    store.remember(database)
    store.remember(storage)
    store.remember(fedora)

    result = retriever.retrieve("database")

    assert result == [database, storage]

    persistence.close()


def test_semantic_retrieval_supports_scope_filter(tmp_path) -> None:
    persistence, store, retriever = create_retriever(tmp_path)

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

    result = retriever.retrieve(
        "database",
        scope=MemoryScope.PROJECT,
    )

    assert result == [project]

    persistence.close()


def test_semantic_retrieval_applies_threshold(tmp_path) -> None:
    persistence, store, retriever = create_retriever(tmp_path)

    memory = Memory(
        content="Tony runs on Fedora.",
        scope=MemoryScope.WORKSPACE,
    )

    store.remember(memory)

    assert retriever.retrieve("database") == []

    persistence.close()


def test_semantic_retrieval_rejects_empty_query(tmp_path) -> None:
    persistence, _, retriever = create_retriever(tmp_path)

    assert retriever.retrieve("") == []
    assert retriever.retrieve("   ") == []

    persistence.close()


def test_cosine_similarity_handles_zero_vectors(tmp_path) -> None:
    persistence, _, retriever = create_retriever(tmp_path)

    assert (
        retriever._cosine_similarity(
            [0.0, 0.0],
            [1.0, 0.0],
        )
        == 0.0
    )

    persistence.close()
