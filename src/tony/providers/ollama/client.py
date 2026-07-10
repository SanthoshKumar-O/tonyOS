"""HTTP client for communicating with a local Ollama server."""

from __future__ import annotations

import httpx
from pydantic import ValidationError

from tony.providers.ollama.exceptions import (
    OllamaConnectionError,
    OllamaRequestError,
    OllamaResponseError,
)
from tony.providers.ollama.models import OllamaGenerateRequest, OllamaGenerateResponse


class OllamaClient:
    def __init__(self, host: str, timeout: int) -> None:

        self.host = host
        self.timeout = timeout
        self._http = httpx.Client(base_url=self.host, timeout=self.timeout)

    def health(self) -> bool:

        try:
            response = self._http.get("/")
        except httpx.RequestError as exc:
            raise OllamaConnectionError(
                f"Could not connect to Ollama server at {self.host}"
            ) from exc

        if response.status_code != httpx.codes.OK:
            raise OllamaResponseError(
                f"Ollama health check failed with status {response.status_code}"
            )

        return True

    def generate(self, request: OllamaGenerateRequest) -> OllamaGenerateResponse:

        try:
            response = self._http.post(
                "/api/generate",
                json=request.model_dump(),
            )
        except httpx.RequestError as exc:
            raise OllamaConnectionError(
                f"Could not connect to Ollama server at {self.host}"
            ) from exc

        if response.status_code == httpx.codes.BAD_REQUEST:
            raise OllamaRequestError(f"Ollama rejected the generate request: {response.text}")

        if response.status_code != httpx.codes.OK:
            raise OllamaResponseError(
                f"Ollama generate request failed with status {response.status_code}"
            )

        try:
            payload = response.json()
        except ValueError as exc:
            raise OllamaResponseError("Ollama returned a non-JSON response") from exc

        try:
            return OllamaGenerateResponse.model_validate(payload)
        except ValidationError as exc:
            raise OllamaResponseError(
                f"Ollama returned an unexpected response shape: {exc}"
            ) from exc

    def close(self) -> None:
        """Closes the underlying HTTP connection pool."""
        self._http.close()
