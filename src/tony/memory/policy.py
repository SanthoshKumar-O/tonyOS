"""Memory retention policy."""

from __future__ import annotations

from tony.memory.models import Memory, MemoryDecision


class DefaultMemoryPolicy:
    """Default deterministic memory retention policy."""

    _TRIVIAL_MESSAGES = frozenset(
        {
            "hi",
            "hello",
            "hey",
            "thanks",
            "thank you",
            "okay",
            "ok",
            "bye",
            "goodbye",
            "yes",
            "no",
            "sure",
            "got it",
            "cool",
            "great",
        }
    )

    def evaluate(self, memory: Memory) -> MemoryDecision:
        """Decide whether a memory contains useful information."""
        normalized = " ".join(memory.content.split()).casefold()

        if normalized in self._TRIVIAL_MESSAGES:
            return MemoryDecision(
                allowed=False,
                reason="Memory is trivial conversational content.",
            )

        return MemoryDecision(
            allowed=True,
            reason="Memory contains potentially useful information.",
        )
