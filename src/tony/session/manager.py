"""Session manager."""

from __future__ import annotations

from uuid import UUID

from tony.conversation import Conversation

from .exceptions import (
    SessionAlreadyExistsError,
    SessionNotFoundError,
)
from .models import Session


class SessionManager:
    """Manages active chat sessions."""

    def __init__(self) -> None:
        self._sessions: dict[UUID, Session] = {}
        self._active: UUID | None = None

    def create(
        self,
        title: str = "New Chat",
    ) -> Session:
        """Create a new session."""

        session = Session(title=title)

        if session.id in self._sessions:
            raise SessionAlreadyExistsError(f"Session '{session.id}' already exists.")

        self._sessions[session.id] = session

        if self._active is None:
            self._active = session.id

        return session

    def delete(
        self,
        session_id: UUID,
    ) -> None:
        """Delete a session."""

        if session_id not in self._sessions:
            raise SessionNotFoundError(f"Session '{session_id}' not found.")

        del self._sessions[session_id]

        if self._active == session_id:
            self._active = next(iter(self._sessions), None)

    def get(
        self,
        session_id: UUID,
    ) -> Session:
        """Return a session."""

        try:
            return self._sessions[session_id]
        except KeyError as exc:
            raise SessionNotFoundError(f"Session '{session_id}' not found.") from exc

    def list(self) -> list[Session]:
        """Return every session."""

        return list(self._sessions.values())

    def active(self) -> Session:
        """Return the active session."""

        if self._active is None:
            raise SessionNotFoundError("No active session.")

        return self.get(self._active)

    def set_active(
        self,
        session_id: UUID,
    ) -> None:
        """Set the active session."""

        if session_id not in self._sessions:
            raise SessionNotFoundError(f"Session '{session_id}' not found.")

        self._active = session_id

    def update_conversation(
        self,
        session_id: UUID,
        conversation: Conversation,
    ) -> Session:
        """Replace a session conversation."""

        session = self.get(session_id)

        updated = session.with_conversation(conversation)

        self._sessions[session_id] = updated

        return updated
