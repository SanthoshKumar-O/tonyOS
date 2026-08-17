from __future__ import annotations

import sqlite3

from tony.persistence import (
    PersistenceConfig,
    SQLitePersistence,
)


def create_persistence(tmp_path) -> SQLitePersistence:
    return SQLitePersistence(
        PersistenceConfig(
            database_path=tmp_path / "tony.db",
        ),
    )


def table_names(database_path) -> set[str]:
    connection = sqlite3.connect(database_path)

    try:
        rows = connection.execute(
            """
            SELECT name
            FROM sqlite_master
            WHERE type = 'table'
            """
        ).fetchall()

        return {row[0] for row in rows}
    finally:
        connection.close()


def test_initialize_creates_database(tmp_path) -> None:
    database_path = tmp_path / "tony.db"

    persistence = create_persistence(tmp_path)
    persistence.initialize()

    assert database_path.exists()

    persistence.close()


def test_initialize_creates_schema(tmp_path) -> None:
    database_path = tmp_path / "tony.db"

    persistence = create_persistence(tmp_path)
    persistence.initialize()
    persistence.close()

    assert {
        "schema_metadata",
        "sessions",
        "conversations",
        "messages",
    }.issubset(table_names(database_path))


def test_initialize_stores_schema_version(tmp_path) -> None:
    database_path = tmp_path / "tony.db"

    persistence = create_persistence(tmp_path)
    persistence.initialize()
    persistence.close()

    connection = sqlite3.connect(database_path)

    try:
        result = connection.execute(
            """
            SELECT value
            FROM schema_metadata
            WHERE key = 'schema_version'
            """
        ).fetchone()

        assert result == ("1",)
    finally:
        connection.close()


def test_initialize_is_idempotent(tmp_path) -> None:
    persistence = create_persistence(tmp_path)

    persistence.initialize()
    persistence.initialize()

    persistence.close()


def test_close_is_idempotent(tmp_path) -> None:
    persistence = create_persistence(tmp_path)

    persistence.initialize()

    persistence.close()
    persistence.close()


def test_database_survives_reopen(tmp_path) -> None:
    database_path = tmp_path / "tony.db"

    first = create_persistence(tmp_path)
    first.initialize()
    first.close()

    second = create_persistence(tmp_path)
    second.initialize()
    second.close()

    assert {
        "schema_metadata",
        "sessions",
        "conversations",
        "messages",
    }.issubset(table_names(database_path))


def test_foreign_keys_are_enabled(tmp_path) -> None:
    database_path = tmp_path / "tony.db"

    persistence = create_persistence(tmp_path)
    persistence.initialize()
    persistence.close()

    connection = sqlite3.connect(database_path)

    try:
        connection.execute("PRAGMA foreign_keys = ON")

        result = connection.execute(
            "PRAGMA foreign_keys"
        ).fetchone()

        assert result == (1,)
    finally:
        connection.close()


def test_session_conversation_relationship_cascades(tmp_path) -> None:
    database_path = tmp_path / "tony.db"

    persistence = create_persistence(tmp_path)
    persistence.initialize()
    persistence.close()

    connection = sqlite3.connect(database_path)

    try:
        connection.execute("PRAGMA foreign_keys = ON")

        connection.execute(
            """
            INSERT INTO sessions (
                id,
                title,
                created_at,
                updated_at
            )
            VALUES (?, ?, ?, ?)
            """,
            ("session-1", "Test", "created", "updated"),
        )

        connection.execute(
            """
            INSERT INTO conversations (session_id)
            VALUES (?)
            """,
            ("session-1",),
        )

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
            ("session-1", "user", "Hello", 0),
        )

        connection.commit()

        connection.execute(
            "DELETE FROM sessions WHERE id = ?",
            ("session-1",),
        )

        conversation_count = connection.execute(
            "SELECT COUNT(*) FROM conversations"
        ).fetchone()

        message_count = connection.execute(
            "SELECT COUNT(*) FROM messages"
        ).fetchone()

        assert conversation_count == (0,)
        assert message_count == (0,)
    finally:
        connection.close()


def test_message_positions_are_unique_per_conversation(tmp_path) -> None:
    database_path = tmp_path / "tony.db"

    persistence = create_persistence(tmp_path)
    persistence.initialize()
    persistence.close()

    connection = sqlite3.connect(database_path)

    try:
        connection.execute("PRAGMA foreign_keys = ON")

        connection.execute(
            """
            INSERT INTO sessions (
                id,
                title,
                created_at,
                updated_at
            )
            VALUES (?, ?, ?, ?)
            """,
            ("session-1", "Test", "created", "updated"),
        )

        connection.execute(
            """
            INSERT INTO conversations (session_id)
            VALUES (?)
            """,
            ("session-1",),
        )

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
            ("session-1", "user", "First", 0),
        )

        try:
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
                ("session-1", "assistant", "Second", 0),
            )
        except sqlite3.IntegrityError:
            pass
        else:
            raise AssertionError(
                "Duplicate message position should fail.",
            )
    finally:
        connection.close()
