from __future__ import annotations

from unittest.mock import Mock, patch

import httpx
import pytest

from tony.providers.ollama.client import OllamaClient
from tony.providers.ollama.exceptions import (
    OllamaConnectionError,
)
from tony.providers.ollama.models import (
    OllamaGenerateRequest,
)


def test_health_returns_true() -> None:
    client = OllamaClient("http://localhost:11434", 120)

    with patch.object(client._http, "get") as mock_get:
        mock_get.return_value = Mock(status_code=httpx.codes.OK)

        assert client.health() is True


def test_health_connection_error() -> None:
    client = OllamaClient("http://localhost:11434", 120)

    with patch.object(client._http, "get") as mock_get:
        mock_get.side_effect = httpx.RequestError(
            "Connection failed",
            request=httpx.Request(
                "GET",
                "http://localhost:11434",
            ),
        )

        with pytest.raises(OllamaConnectionError):
            client.health()


def test_generate_returns_response() -> None:
    client = OllamaClient("http://localhost:11434", 120)

    request = OllamaGenerateRequest(
        model="qwen3:8b",
        prompt="Hello",
    )

    payload = {
        "model": "qwen3:8b",
        "response": "Hello!",
        "done": True,
    }

    response = Mock(
        status_code=httpx.codes.OK,
    )

    response.json.return_value = payload

    with patch.object(client._http, "post") as mock_post:
        mock_post.return_value = response

        result = client.generate(request)

        assert result.response == "Hello!"
        assert result.model == "qwen3:8b"
        assert result.done is True
