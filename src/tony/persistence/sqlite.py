"""SQLite persistence implementation."""

from __future__ import annotations

import sqlite3

from .exceptions import (
    PersistenceConnectionError,
    PersistenceInitializationError,
)
from .models import PersistenceConfig
from .protocols import PersistenceProtocol


class SQLitePersistence(PersistenceProtocol):
    """SQLite-backed persistence lifecycle."""

    SCHEMA_VERSION = "1"

    def __init__(self, config: PersistenceConfig) -> None:
        self._config = config
        self._connection: sqlite3.Connection | None = None

    def initialize(self) -> None:
        """Open the database and initialize its schema."""

        if self._connection is not None:
            return

        try:
            self._config.database_path.parent.mkdir(
                parents=True,
                exist_ok=True,
            )

            self._connection = sqlite3.connect(
                self._config.database_path,
            )
        except sqlite3.Error as exc:
            raise PersistenceConnectionError(
                "Failed to connect to SQLite database.",
            ) from exc
        except OSError as exc:
            raise PersistenceConnectionError(
                "Failed to prepare SQLite database path.",
            ) from exc

        try:
            self._connection.execute("PRAGMA foreign_keys = ON")
            self._initialize_schema()
            self._connection.commit()
        except sqlite3.Error as exc:
            self.close()
            raise PersistenceInitializationError(
                "Failed to initialize SQLite schema.",
            ) from exc

    @property
    def connection(self) -> sqlite3.Connection:
        """Return the active database connection."""

        if self._connection is None:
            raise PersistenceConnectionError(
                "SQLite persistence is not initialized.",
            )

        return self._connection

    def close(self) -> None:
        """Close the database connection."""

        if self._connection is None:
            return

        self._connection.close()
        self._connection = None

    def _initialize_schema(self) -> None:
        """Create the Tony persistence schema."""

        assert self._connection is not None

        self._connection.execute(
            """
            CREATE TABLE IF NOT EXISTS schema_metadata (
                key TEXT PRIMARY KEY,
                value TEXT NOT NULL
            )
            """
        )

        self._connection.execute(
            """
            CREATE TABLE IF NOT EXISTS sessions (
                id TEXT PRIMARY KEY,
                title TEXT NOT NULL,
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL
            )
            """
        )

        self._connection.execute(
            """
            CREATE TABLE IF NOT EXISTS conversations (
                session_id TEXT PRIMARY KEY,
                FOREIGN KEY(session_id)
                    REFERENCES sessions(id)
                    ON DELETE CASCADE
            )
            """
        )

        self._connection.execute(
            """
            CREATE TABLE IF NOT EXISTS messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                conversation_id TEXT NOT NULL,
                role TEXT NOT NULL,
                content TEXT NOT NULL,
                position INTEGER NOT NULL,
                FOREIGN KEY(conversation_id)
                    REFERENCES conversations(session_id)
                    ON DELETE CASCADE,
                UNIQUE(conversation_id, position)
            )
            """
        )

        self._connection.execute(
            """
            CREATE TABLE IF NOT EXISTS memories (
                id TEXT PRIMARY KEY,
                content TEXT NOT NULL,
                scope TEXT NOT NULL,
                created_at TEXT NOT NULL
            )
            """
        )

        self._connection.execute(
            """
            CREATE TABLE IF NOT EXISTS memory_embeddings (
                memory_id TEXT PRIMARY KEY,
                embedding TEXT NOT NULL,
                FOREIGN KEY(memory_id)
                    REFERENCES memories(id)
                    ON DELETE CASCADE
            )
            """
        )

        self._connection.execute(
            """
            INSERT INTO schema_metadata (key, value)
            VALUES ('schema_version', ?)
            ON CONFLICT(key) DO UPDATE SET value = excluded.value
            """,
            (self.SCHEMA_VERSION,),
        )
