"""Pydantic models for Ollama API requests and responses."""

from __future__ import annotations

from pydantic import BaseModel


class OllamaGenerateRequest(BaseModel):
    """Request payload for the Ollama ``/api/generate`` endpoint.

    Attributes:
        model: Name of the model to use for generation.
        prompt: Prompt text to send to the model.
        stream: Whether to stream the response. Always False for M1.6.
    """

    model: str
    prompt: str
    stream: bool = False


class OllamaGenerateResponse(BaseModel):
    """Response payload from the Ollama ``/api/generate`` endpoint.

    Attributes:
        model: Name of the model that generated the response.
        response: Generated text.
        done: Whether generation has completed.
    """

    model: str
    response: str
    done: bool
