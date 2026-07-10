from __future__ import annotations

from unittest.mock import Mock, patch

import pytest

from tony.providers.exceptions import (
    ProviderInitializationError,
)
from tony.providers.ollama.provider import (
    OllamaProvider,
)


def make_provider() -> OllamaProvider:
    return OllamaProvider(
        host="http://localhost:11434",
        model="qwen3:8b",
        timeout=120,
    )


def test_initialize_marks_provider_initialized() -> None:
    provider = make_provider()

    with patch("tony.providers.ollama.provider.OllamaClient") as mock_client:
        instance = mock_client.return_value
        instance.health.return_value = True

        provider.initialize()

        assert provider.initialized is True


def test_shutdown_marks_provider_shutdown() -> None:
    provider = make_provider()

    with patch("tony.providers.ollama.provider.OllamaClient") as mock_client:
        instance = mock_client.return_value
        instance.health.return_value = True

        provider.initialize()
        provider.shutdown()

        assert provider.initialized is False


def test_generate_requires_initialization() -> None:
    provider = make_provider()

    with pytest.raises(ProviderInitializationError):
        provider.generate("Hello")


def test_generate_returns_text() -> None:
    provider = make_provider()

    with patch("tony.providers.ollama.provider.OllamaClient") as mock_client:
        instance = mock_client.return_value

        instance.health.return_value = True
        instance.generate.return_value = Mock(response="Tony is alive!")

        provider.initialize()

        result = provider.generate("Hello")

        assert result == "Tony is alive!"
