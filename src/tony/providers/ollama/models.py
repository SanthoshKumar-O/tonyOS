"""Pydantic models for Ollama API requests and responses."""

from __future__ import annotations

from pydantic import BaseModel


class OllamaGenerateRequest(BaseModel):
    """Request payload for the Ollama ``/api/generate`` endpoint."""

    model: str
    prompt: str
    stream: bool = False


class OllamaGenerateResponse(BaseModel):
    """Response payload from the Ollama ``/api/generate`` endpoint."""

    model: str
    response: str
    done: bool


class OllamaEmbedRequest(BaseModel):
    """Request payload for the Ollama ``/api/embed`` endpoint."""

    model: str
    input: str


class OllamaEmbedResponse(BaseModel):
    """Response payload from the Ollama ``/api/embed`` endpoint."""

    model: str
    embeddings: list[list[float]]
