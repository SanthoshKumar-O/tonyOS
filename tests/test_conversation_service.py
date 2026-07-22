from __future__ import annotations

from tony.conversation import (
    Conversation,
    ConversationService,
    MessageRole,
)


class DummyPromptBuilder:
    def build(
        self,
        conversation: Conversation,
    ) -> str:
        return "dummy prompt"


class DummyLLMService:
    def generate(
        self,
        prompt: str,
    ) -> str:
        return "Hello from Tony!"


def test_reply_adds_user_and_assistant_messages() -> None:
    service = ConversationService(
        prompt_builder=DummyPromptBuilder(),
        llm_service=DummyLLMService(),
    )

    conversation = Conversation()

    conversation = service.reply(
        conversation,
        "Hello",
    )

    assert conversation.message_count() == 2

    messages = conversation.messages

    assert messages[0].role == MessageRole.USER
    assert messages[0].content == "Hello"

    assert messages[1].role == MessageRole.ASSISTANT
    assert messages[1].content == "Hello from Tony!"


def test_reply_returns_new_conversation() -> None:
    service = ConversationService(
        prompt_builder=DummyPromptBuilder(),
        llm_service=DummyLLMService(),
    )

    original = Conversation()

    updated = service.reply(
        original,
        "Hi",
    )

    assert original.message_count() == 0
    assert updated.message_count() == 2


def test_multiple_replies_extend_conversation() -> None:
    service = ConversationService(
        prompt_builder=DummyPromptBuilder(),
        llm_service=DummyLLMService(),
    )

    conversation = Conversation()

    conversation = service.reply(
        conversation,
        "One",
    )

    conversation = service.reply(
        conversation,
        "Two",
    )

    assert conversation.message_count() == 4

    assert conversation.messages[0].content == "One"
    assert conversation.messages[1].content == "Hello from Tony!"
    assert conversation.messages[2].content == "Two"
    assert conversation.messages[3].content == "Hello from Tony!"
