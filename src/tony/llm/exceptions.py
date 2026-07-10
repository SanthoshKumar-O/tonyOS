"""Exceptions for the LLM service."""

from __future__ import annotations


class LLMError(Exception):
    """Base exception for the LLM service."""


class LLMInitializationError(LLMError):
    """Raised when the LLM service is not initialized correctly."""


class LLMGenerationError(LLMError):
    """Raised when text generation fails."""
