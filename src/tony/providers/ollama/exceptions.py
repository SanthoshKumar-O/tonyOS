"""Exception types for the Ollama provider."""

from __future__ import annotations


class OllamaError(Exception):
    """Base exception for all Ollama provider errors."""


class OllamaConnectionError(OllamaError):
    """Raised when the Ollama server cannot be reached."""


class OllamaRequestError(OllamaError):
    """Raised when a request to the Ollama server is malformed or rejected."""


class OllamaResponseError(OllamaError):
    """Raised when the Ollama server returns an invalid or unexpected response."""
