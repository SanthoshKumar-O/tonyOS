"""Session manager."""

from __future__ import annotations

from typing import TYPE_CHECKING
from uuid import UUID

from tony.conversation import Conversation

if TYPE_CHECKING:
    from tony.persistence.repository import SessionRepository

from .exceptions import (
    SessionAlreadyExistsError,
    SessionNotFoundError,
)
from .models import Session


class SessionManager:
    """Manages active chat sessions."""

    def __init__(
        self,
        repository: SessionRepository | None = None,
    ) -> None:
        self._sessions: dict[UUID, Session] = {}
        self._active: UUID | None = None
        self._repository = repository

        if self._repository is not None:
            persisted_sessions = self._repository.list()
            self._sessions = {
                session.id: session
                for session in persisted_sessions
            }

            if persisted_sessions:
                self._active = persisted_sessions[0].id

    def create(
        self,
        title: str = "New Chat",
    ) -> Session:
        """Create a new session."""

        session = Session(title=title)

        if session.id in self._sessions:
            raise SessionAlreadyExistsError(
                f"Session '{session.id}' already exists.",
            )

        if self._repository is not None:
            self._repository.save(session)

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
            raise SessionNotFoundError(
                f"Session '{session_id}' not found.",
            )

        if self._repository is not None:
            self._repository.delete(session_id)

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
            raise SessionNotFoundError(
                f"Session '{session_id}' not found.",
            ) from exc

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
            raise SessionNotFoundError(
                f"Session '{session_id}' not found.",
            )

        self._active = session_id

    def update_conversation(
        self,
        session_id: UUID,
        conversation: Conversation,
    ) -> Session:
        """Replace a session conversation."""

        session = self.get(session_id)

        updated = session.with_conversation(conversation)

        if self._repository is not None:
            self._repository.save(updated)

        self._sessions[session_id] = updated

        return updated
