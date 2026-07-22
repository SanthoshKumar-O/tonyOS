from __future__ import annotations

import pytest
from pydantic import ValidationError

from tony.conversation import Conversation
from tony.session import Session


def test_default_session() -> None:
    session = Session()

    assert session.title == "New Chat"
    assert isinstance(session.conversation, Conversation)


def test_with_conversation_returns_new_session() -> None:
    session = Session()

    conversation = Conversation()

    updated = session.with_conversation(conversation)

    assert updated is not session
    assert updated.conversation == conversation
    assert updated.metadata.updated_at >= session.metadata.updated_at


def test_session_is_immutable() -> None:
    session = Session()

    with pytest.raises(ValidationError):
        session.title = "Changed"
