"""SQLite session repository implementation."""

from __future__ import annotations

from datetime import datetime
from uuid import UUID

from tony.conversation import Conversation, Message, MessageRole
from tony.session import Session, SessionMetadata

from .repository import SessionRepository
from .repository_exceptions import (
    SessionNotPersistedError,
    SessionPersistenceError,
)
from .sqlite import SQLitePersistence


class SQLiteSessionRepository(SessionRepository):
    """Persists Tony sessions using SQLite."""

    def __init__(self, persistence: SQLitePersistence) -> None:
        self._persistence = persistence

    @property
    def _connection(self):
        """Return the active persistence connection."""

        return self._persistence.connection

    def save(self, session: Session) -> None:
        """Persist a complete session."""

        try:
            connection = self._connection

            connection.execute(
                """
                INSERT INTO sessions (
                    id,
                    title,
                    created_at,
                    updated_at
                )
                VALUES (?, ?, ?, ?)
                ON CONFLICT(id) DO UPDATE SET
                    title = excluded.title,
                    created_at = excluded.created_at,
                    updated_at = excluded.updated_at
                """,
                (
                    str(session.id),
                    session.title,
                    session.metadata.created_at.isoformat(),
                    session.metadata.updated_at.isoformat(),
                ),
            )

            connection.execute(
                """
                INSERT INTO conversations (session_id)
                VALUES (?)
                ON CONFLICT(session_id) DO NOTHING
                """,
                (str(session.id),),
            )

            connection.execute(
                "DELETE FROM messages WHERE conversation_id = ?",
                (str(session.id),),
            )

            for position, message in enumerate(session.conversation.messages):
                connection.execute(
                    """
                    INSERT INTO messages (
                        conversation_id,
                        role,
                        content,
                        position
                    )
                    VALUES (?, ?, ?, ?)
                    """,
                    (
                        str(session.id),
                        message.role.value,
                        message.content,
                        position,
                    ),
                )

            connection.commit()

        except Exception as exc:
            connection.rollback()
            raise SessionPersistenceError(
                f"Failed to persist session '{session.id}'.",
            ) from exc

    def get(self, session_id: UUID) -> Session:
        """Retrieve a session by ID."""

        try:
            session_row = self._connection.execute(
                """
                SELECT
                    id,
                    title,
                    created_at,
                    updated_at
                FROM sessions
                WHERE id = ?
                """,
                (str(session_id),),
            ).fetchone()

            if session_row is None:
                raise SessionNotPersistedError(
                    f"Session '{session_id}' is not persisted.",
                )

            message_rows = self._connection.execute(
                """
                SELECT
                    role,
                    content
                FROM messages
                WHERE conversation_id = ?
                ORDER BY position
                """,
                (str(session_id),),
            ).fetchall()

            conversation = Conversation(
                messages=tuple(
                    Message(
                        role=MessageRole(row[0]),
                        content=row[1],
                    )
                    for row in message_rows
                ),
            )

            return Session(
                id=UUID(session_row[0]),
                title=session_row[1],
                conversation=conversation,
                metadata=SessionMetadata(
                    created_at=datetime.fromisoformat(session_row[2]),
                    updated_at=datetime.fromisoformat(session_row[3]),
                ),
            )

        except SessionNotPersistedError:
            raise
        except Exception as exc:
            raise SessionPersistenceError(
                f"Failed to load session '{session_id}'.",
            ) from exc

    def list(self) -> list[Session]:
        """Return all persisted sessions."""

        try:
            rows = self._connection.execute(
                """
                SELECT id
                FROM sessions
                ORDER BY created_at, id
                """
            ).fetchall()

            return [self.get(UUID(row[0])) for row in rows]

        except SessionPersistenceError:
            raise
        except Exception as exc:
            raise SessionPersistenceError(
                "Failed to list persisted sessions.",
            ) from exc

    def delete(self, session_id: UUID) -> None:
        """Delete a persisted session."""

        try:
            cursor = self._connection.execute(
                """
                DELETE FROM sessions
                WHERE id = ?
                """,
                (str(session_id),),
            )

            if cursor.rowcount == 0:
                raise SessionNotPersistedError(
                    f"Session '{session_id}' is not persisted.",
                )

            self._connection.commit()

        except SessionNotPersistedError:
            raise
        except Exception as exc:
            self._connection.rollback()
            raise SessionPersistenceError(
                f"Failed to delete session '{session_id}'.",
            ) from exc

    def exists(self, session_id: UUID) -> bool:
        """Return whether a session exists."""

        try:
            result = self._connection.execute(
                """
                SELECT 1
                FROM sessions
                WHERE id = ?
                """,
                (str(session_id),),
            ).fetchone()

            return result is not None

        except Exception as exc:
            raise SessionPersistenceError(
                f"Failed to check session '{session_id}'.",
            ) from exc
