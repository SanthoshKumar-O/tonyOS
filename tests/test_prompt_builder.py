from __future__ import annotations

from tony.conversation import Conversation, Message, MessageRole
from tony.prompts import Prompt, PromptBuilder


class DummyPromptManager:
    def get(self, name: str) -> Prompt:
        return Prompt(
            name="system",
            content="You are Tony.",
        )


def test_build_empty_conversation() -> None:
    builder = PromptBuilder(
        DummyPromptManager(),
    )

    conversation = Conversation()

    result = builder.build(conversation)

    assert "You are Tony." in result


def test_build_single_message() -> None:
    builder = PromptBuilder(
        DummyPromptManager(),
    )

    conversation = Conversation()

    conversation = conversation.add(
        Message(
            role=MessageRole.USER,
            content="Hello",
        )
    )

    result = builder.build(conversation)

    assert "user:" in result
    assert "Hello" in result


def test_build_multiple_messages() -> None:
    builder = PromptBuilder(
        DummyPromptManager(),
    )

    conversation = Conversation()

    conversation = conversation.add(
        Message(
            role=MessageRole.USER,
            content="Hello",
        )
    )

    conversation = conversation.add(
        Message(
            role=MessageRole.ASSISTANT,
            content="Hi!",
        )
    )

    result = builder.build(conversation)

    assert "user:" in result
    assert "assistant:" in result
    assert "Hello" in result
    assert "Hi!" in result
