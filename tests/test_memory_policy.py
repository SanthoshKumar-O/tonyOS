from __future__ import annotations

import pytest

from tony.memory import (
    DefaultMemoryPolicy,
    Memory,
    MemoryScope,
)


def test_default_memory_policy_allows_memory() -> None:
    policy = DefaultMemoryPolicy()

    memory = Memory(
        content="Tony is local-first.",
        scope=MemoryScope.PROJECT,
    )

    decision = policy.evaluate(memory)

    assert decision.allowed is True
    assert "useful" in decision.reason.lower()


@pytest.mark.parametrize(
    "content",
    [
        "hi",
        "hello",
        "thanks",
        "thank you",
        "okay",
        "ok",
        "bye",
        "goodbye",
        "got it",
    ],
)
def test_default_memory_policy_rejects_trivial_conversation(
    content: str,
) -> None:
    policy = DefaultMemoryPolicy()

    memory = Memory(
        content=content,
        scope=MemoryScope.CONVERSATION,
    )

    decision = policy.evaluate(memory)

    assert decision.allowed is False
    assert "trivial" in decision.reason.lower()


def test_default_memory_policy_normalizes_trivial_content() -> None:
    policy = DefaultMemoryPolicy()

    memory = Memory(
        content="  THANKS   ",
        scope=MemoryScope.CONVERSATION,
    )

    decision = policy.evaluate(memory)

    assert decision.allowed is False


def test_default_memory_policy_allows_short_meaningful_memory() -> None:
    policy = DefaultMemoryPolicy()

    memory = Memory(
        content="Use SQLite.",
        scope=MemoryScope.PROJECT,
    )

    decision = policy.evaluate(memory)

    assert decision.allowed is True
