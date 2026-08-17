
from __future__ import annotations

from datetime import UTC, datetime

import pytest

from tony.conversation import Conversation, Message, MessageRole
from tony.persistence import (
    PersistenceConfig,
    SessionNotPersistedError,
    SQLitePersistence,
    SQLiteSessionRepository,
)
from tony.session import Session, SessionMetadata


def create_repository(
    tmp_path,
) -> tuple[SQLitePersistence, SQLiteSessionRepository]:
    persistence = SQLitePersistence(
        PersistenceConfig(
            database_path=tmp_path / "tony.db",
        ),
    )
    persistence.initialize()

    return persistence, SQLiteSessionRepository(persistence)


def test_save_and_get_session(tmp_path) -> None:
    persistence, repository = create_repository(tmp_path)

    session = Session(title="Project Tony")

    repository.save(session)

    loaded = repository.get(session.id)

    assert loaded == session

    persistence.close()


def test_save_and_get_conversation(tmp_path) -> None:
    persistence, repository = create_repository(tmp_path)

    conversation = Conversation(
        messages=(
            Message(
                role=MessageRole.SYSTEM,
                content="You are Tony.",
            ),
            Message(
                role=MessageRole.USER,
                content="Hello",
            ),
            Message(
                role=MessageRole.ASSISTANT,
                content="Hello from Tony!",
            ),
        ),
    )

    session = Session(
        title="Conversation Test",
        conversation=conversation,
    )

    repository.save(session)

    loaded = repository.get(session.id)

    assert loaded.conversation == conversation

    persistence.close()


def test_save_preserves_metadata(tmp_path) -> None:
    persistence, repository = create_repository(tmp_path)

    created_at = datetime(2026, 8, 1, 10, 30, tzinfo=UTC)
    updated_at = datetime(2026, 8, 2, 12, 45, tzinfo=UTC)

    session = Session(
        metadata=SessionMetadata(
            created_at=created_at,
            updated_at=updated_at,
        ),
    )

    repository.save(session)

    loaded = repository.get(session.id)

    assert loaded.metadata.created_at == created_at
    assert loaded.metadata.updated_at == updated_at

    persistence.close()


def test_save_updates_existing_session(tmp_path) -> None:
    persistence, repository = create_repository(tmp_path)

    session = Session(title="Original")

    repository.save(session)

    updated = session.model_copy(
        update={
            "title": "Updated",
        },
    )

    repository.save(updated)

    loaded = repository.get(session.id)

    assert loaded.title == "Updated"

    persistence.close()


def test_save_replaces_messages(tmp_path) -> None:
    persistence, repository = create_repository(tmp_path)

    original = Session(
        conversation=Conversation(
            messages=(
                Message(
                    role=MessageRole.USER,
                    content="First",
                ),
            ),
        ),
    )

    repository.save(original)

    updated = original.with_conversation(
        Conversation(
            messages=(
                Message(
                    role=MessageRole.USER,
                    content="Second",
                ),
            ),
        ),
    )

    repository.save(updated)

    loaded = repository.get(original.id)

    assert loaded.conversation.message_count() == 1

    last_message = loaded.conversation.last_message()

    assert last_message is not None
    assert last_message.content == "Second"

    persistence.close()


def test_list_sessions(tmp_path) -> None:
    persistence, repository = create_repository(tmp_path)

    first = Session(title="First")
    second = Session(title="Second")

    repository.save(first)
    repository.save(second)

    sessions = repository.list()

    assert len(sessions) == 2
    assert {session.id for session in sessions} == {
        first.id,
        second.id,
    }

    persistence.close()


def test_exists(tmp_path) -> None:
    persistence, repository = create_repository(tmp_path)

    session = Session()

    assert repository.exists(session.id) is False

    repository.save(session)

    assert repository.exists(session.id) is True

    persistence.close()


def test_delete_session(tmp_path) -> None:
    persistence, repository = create_repository(tmp_path)

    session = Session()

    repository.save(session)

    repository.delete(session.id)

    assert repository.exists(session.id) is False

    persistence.close()


def test_delete_missing_session_raises(tmp_path) -> None:
    persistence, repository = create_repository(tmp_path)

    session_id = Session().id

    with pytest.raises(SessionNotPersistedError):
        repository.delete(session_id)

    persistence.close()


def test_get_missing_session_raises(tmp_path) -> None:
    persistence, repository = create_repository(tmp_path)

    session_id = Session().id

    with pytest.raises(SessionNotPersistedError):
        repository.get(session_id)

    persistence.close()


def test_delete_cascades_conversation_and_messages(tmp_path) -> None:
    persistence, repository = create_repository(tmp_path)

    session = Session(
        conversation=Conversation(
            messages=(
                Message(
                    role=MessageRole.USER,
                    content="Hello",
                ),
            ),
        ),
    )

    repository.save(session)
    repository.delete(session.id)

    connection = persistence.connection

    conversation_count = connection.execute(
        "SELECT COUNT(*) FROM conversations",
    ).fetchone()

    message_count = connection.execute(
        "SELECT COUNT(*) FROM messages",
    ).fetchone()

    assert conversation_count == (0,)
    assert message_count == (0,)

    persistence.close()


def test_repository_round_trip_after_reopen(tmp_path) -> None:
    persistence, repository = create_repository(tmp_path)

    session = Session(
        title="Persistent Tony",
        conversation=Conversation(
            messages=(
                Message(
                    role=MessageRole.USER,
                    content="Remember this.",
                ),
                Message(
                    role=MessageRole.ASSISTANT,
                    content="I have it.",
                ),
            ),
        ),
    )

    repository.save(session)
    persistence.close()

    reopened, repository = create_repository(tmp_path)

    loaded = repository.get(session.id)

    assert loaded == session

    reopened.close()
