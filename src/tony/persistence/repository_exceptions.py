"""Persistence repository exceptions."""

from __future__ import annotations


class RepositoryError(Exception):
    """Base exception for repository operations."""


class SessionPersistenceError(RepositoryError):
    """Raised when a session cannot be persisted."""


class SessionNotPersistedError(RepositoryError):
    """Raised when a requested persisted session does not exist."""
