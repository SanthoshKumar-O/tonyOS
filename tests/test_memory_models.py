from __future__ import annotations

import pytest
from pydantic import ValidationError

from tony.memory import InvalidMemoryError, Memory, MemoryDecision, MemoryScope


def test_memory_defaults() -> None:
    memory = Memory(
        content="Tony uses SQLite for persistence.",
        scope=MemoryScope.PROJECT,
    )

    assert memory.content == "Tony uses SQLite for persistence."
    assert memory.scope is MemoryScope.PROJECT
    assert memory.id is not None
    assert memory.created_at.tzinfo is not None


def test_memory_scopes() -> None:
    assert MemoryScope.WORKING.value == "working"
    assert MemoryScope.CONVERSATION.value == "conversation"
    assert MemoryScope.PROJECT.value == "project"
    assert MemoryScope.WORKSPACE.value == "workspace"
    assert MemoryScope.SEMANTIC.value == "semantic"


def test_memory_rejects_empty_content() -> None:
    with pytest.raises(InvalidMemoryError):
        Memory(
            content="",
            scope=MemoryScope.WORKING,
        )


def test_memory_rejects_whitespace_content() -> None:
    with pytest.raises(InvalidMemoryError):
        Memory(
            content="   ",
            scope=MemoryScope.WORKING,
        )


def test_memory_is_immutable() -> None:
    memory = Memory(
        content="Tony is local-first.",
        scope=MemoryScope.PROJECT,
    )

    with pytest.raises(ValidationError):
        memory.content = "Changed"


def test_memory_has_unique_ids() -> None:
    first = Memory(
        content="First memory",
        scope=MemoryScope.WORKING,
    )
    second = Memory(
        content="Second memory",
        scope=MemoryScope.WORKING,
    )

    assert first.id != second.id


def test_memory_decision_is_immutable() -> None:
    decision = MemoryDecision(
        allowed=True,
        reason="Memory is permitted.",
    )

    with pytest.raises(ValidationError):
        decision.allowed = False
