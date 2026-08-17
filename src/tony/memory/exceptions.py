"""Memory exceptions."""

from __future__ import annotations


class MemoryError(Exception):
    """Base exception for memory operations."""


class InvalidMemoryError(MemoryError):
    """Raised when a memory is invalid."""
