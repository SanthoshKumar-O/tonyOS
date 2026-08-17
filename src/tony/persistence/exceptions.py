"""Persistence exceptions."""

from __future__ import annotations


class PersistenceError(Exception):
    """Base exception for persistence operations."""


class PersistenceConnectionError(PersistenceError):
    """Raised when a persistence connection cannot be established."""


class PersistenceInitializationError(PersistenceError):
    """Raised when persistence initialization fails."""
