from __future__ import annotations

from tony.memory import EmbeddingProvider


class DummyEmbeddingProvider:
    """In-memory implementation used to verify the embedding contract."""

    def embed(self, text: str) -> list[float]:
        return [float(len(text))]


def test_embedding_provider_protocol() -> None:
    provider: EmbeddingProvider = DummyEmbeddingProvider()

    result = provider.embed("Tony")

    assert result == [4.0]


def test_embedding_provider_returns_vector() -> None:
    provider: EmbeddingProvider = DummyEmbeddingProvider()

    result = provider.embed("Tony is local-first.")

    assert isinstance(result, list)
    assert all(isinstance(value, float) for value in result)
