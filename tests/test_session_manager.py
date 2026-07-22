from __future__ import annotations

import pytest

from tony.conversation import Conversation
from tony.session import (
    SessionManager,
    SessionNotFoundError,
)


def test_create_session() -> None:
    manager = SessionManager()

    session = manager.create()

    assert session.title == "New Chat"
    assert len(manager.list()) == 1


def test_create_named_session() -> None:
    manager = SessionManager()

    session = manager.create("Project Tony")

    assert session.title == "Project Tony"


def test_get_session() -> None:
    manager = SessionManager()

    created = manager.create()

    loaded = manager.get(created.id)

    assert loaded == created


def test_active_session() -> None:
    manager = SessionManager()

    created = manager.create()

    assert manager.active() == created


def test_switch_active_session() -> None:
    manager = SessionManager()

    first = manager.create("First")
    second = manager.create("Second")

    manager.set_active(second.id)

    assert manager.active() == second
    assert manager.active() != first


def test_delete_session() -> None:
    manager = SessionManager()

    session = manager.create()

    manager.delete(session.id)

    assert manager.list() == []


def test_delete_missing_session() -> None:
    manager = SessionManager()

    session = manager.create()

    manager.delete(session.id)

    with pytest.raises(SessionNotFoundError):
        manager.get(session.id)


def test_update_conversation() -> None:
    manager = SessionManager()

    session = manager.create()

    conversation = Conversation()

    updated = manager.update_conversation(
        session.id,
        conversation,
    )

    assert updated.conversation == conversation


def test_list_sessions() -> None:
    manager = SessionManager()

    manager.create("One")
    manager.create("Two")
    manager.create("Three")

    assert len(manager.list()) == 3


def test_no_active_session() -> None:
    manager = SessionManager()

    with pytest.raises(SessionNotFoundError):
        manager.active()
