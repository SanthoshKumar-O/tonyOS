"""Exceptions for the streaming system."""

from __future__ import annotations


class StreamingError(Exception):
    """Base exception for the streaming system."""


class StreamGenerationError(StreamingError):
    """Raised when a response stream cannot be generated."""
