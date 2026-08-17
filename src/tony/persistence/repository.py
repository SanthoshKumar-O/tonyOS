"""Session persistence repository protocol."""

from __future__ import annotations

from typing import Protocol
from uuid import UUID

from tony.session import Session


class SessionRepository(Protocol):
    """Protocol for persistent session storage."""

    def save(self, session: Session) -> None:
        """Persist a session."""
        ...

    def get(self, session_id: UUID) -> Session:
        """Retrieve a persisted session."""
        ...

    def list(self) -> list[Session]:
        """Return all persisted sessions."""
        ...

    def delete(self, session_id: UUID) -> None:
        """Delete a persisted session."""
        ...

    def exists(self, session_id: UUID) -> bool:
        """Return whether a persisted session exists."""
        ...
