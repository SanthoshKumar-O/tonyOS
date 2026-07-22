"""Session exceptions."""

from __future__ import annotations


class SessionError(Exception):
    """Base exception for session management."""


class SessionNotFoundError(SessionError):
    """Raised when a session cannot be found."""


class SessionAlreadyExistsError(SessionError):
    """Raised when a duplicate session is created."""
