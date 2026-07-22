from __future__ import annotations

import pytest

from tony.conversation import Conversation, Message, MessageRole
from tony.conversation.exceptions import InvalidMessageError


def test_empty_conversation() -> None:
    conversation = Conversation()

    assert conversation.message_count() == 0
    assert conversation.last_message() is None
    assert conversation.system_prompt() is None


def test_add_user_message() -> None:
    conversation = Conversation()

    message = Message(
        role=MessageRole.USER,
        content="Hello",
    )

    updated = conversation.add(message)

    assert conversation.message_count() == 0
    assert updated.message_count() == 1
    assert updated.last_message() == message


def test_add_assistant_message() -> None:
    conversation = Conversation()

    conversation = conversation.add(Message(role=MessageRole.ASSISTANT, content="Hi"))

    last_message = conversation.last_message()
    assert last_message is not None
    assert last_message.role == MessageRole.ASSISTANT


def test_system_prompt() -> None:
    conversation = Conversation()

    system = Message(
        role=MessageRole.SYSTEM,
        content="You are Tony.",
    )

    conversation = conversation.add(system)

    message = conversation.system_prompt()
    assert message is not None
    assert message.content == "You are Tony."


def test_message_count() -> None:
    conversation = Conversation()

    conversation = conversation.add(Message(role=MessageRole.USER, content="A"))

    conversation = conversation.add(Message(role=MessageRole.ASSISTANT, content="B"))

    assert conversation.message_count() == 2


def test_empty_message_raises() -> None:
    with pytest.raises(InvalidMessageError):
        Message(
            role=MessageRole.USER,
            content="",
        )


def test_conversation_is_immutable() -> None:
    original = Conversation()

    updated = original.add(Message(role=MessageRole.USER, content="Hello"))

    assert original.message_count() == 0
    assert updated.message_count() == 1
