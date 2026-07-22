"""Protocols for Tony's intelligence pipeline."""

from __future__ import annotations

from collections.abc import Iterator
from typing import Protocol

from tony.context import ExecutionContext
from tony.streaming import StreamChunk


class IntelligencePipelineProtocol(Protocol):
    """Coordinates Tony's intelligence pipeline."""

    def execute(
        self,
        context: ExecutionContext,
    ) -> Iterator[StreamChunk]: ...
