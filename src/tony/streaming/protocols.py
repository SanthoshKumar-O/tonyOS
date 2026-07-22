"""Protocols for the streaming system."""

from __future__ import annotations

from collections.abc import Iterator
from typing import Protocol

from tony.response import Response

from .models import (
    StreamChunk,
)


class ResponseStreamerProtocol(Protocol):
    """Streams responses."""

    def stream(
        self,
        response: Response,
    ) -> Iterator[StreamChunk]: ...
