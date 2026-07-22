"""Exceptions for the clarification system."""

from __future__ import annotations


class ClarificationError(Exception):
    """Base exception for the clarification system."""


class ClarificationGenerationError(ClarificationError):
    """Raised when a clarification request cannot be generated."""
