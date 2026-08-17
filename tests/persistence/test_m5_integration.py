from __future__ import annotations

from tony.conversation import Conversation, Message, MessageRole
from tony.persistence import (
    PersistenceConfig,
    SQLitePersistence,
    SQLiteSessionRepository,
)
from tony.session import Session


def test_session_survives_persistence_restart(tmp_path) -> None:
    database_path = tmp_path / "tony.db"

    # First application lifetime.
    persistence_a = SQLitePersistence(
        PersistenceConfig(database_path=database_path),
    )
    persistence_a.initialize()

    repository_a = SQLiteSessionRepository(persistence_a)

    session = Session(
        title="M5 persistence test",
    )

    conversation = Conversation()
    conversation = conversation.add(
        Message(
            role=MessageRole.USER,
            content="Remember that Tony is local-first.",
        ),
    )
    conversation = conversation.add(
        Message(
            role=MessageRole.ASSISTANT,
            content="I will retain that in the session.",
        ),
    )

    session = session.with_conversation(conversation)

    repository_a.save(session)

    session_id = session.id

    assert repository_a.exists(session_id)
    assert repository_a.get(session_id) == session

    persistence_a.close()

    # Simulated application restart.
    persistence_b = SQLitePersistence(
        PersistenceConfig(database_path=database_path),
    )
    persistence_b.initialize()

    repository_b = SQLiteSessionRepository(persistence_b)

    restored = repository_b.get(session_id)

    assert restored.id == session.id
    assert restored.title == session.title
    assert restored.conversation.messages == session.conversation.messages
    assert len(restored.conversation.messages) == 2

    assert restored.conversation.messages[0].role is MessageRole.USER
    assert (
        restored.conversation.messages[0].content
        == "Remember that Tony is local-first."
    )

    assert restored.conversation.messages[1].role is MessageRole.ASSISTANT
    assert (
        restored.conversation.messages[1].content
        == "I will retain that in the session."
    )

    persistence_b.close()
