"""Streaming models."""

from __future__ import annotations

from enum import StrEnum

from pydantic import BaseModel, ConfigDict


class StreamEvent(StrEnum):
    """Supported stream events."""

    START = "start"
    CHUNK = "chunk"
    END = "end"


class StreamChunk(BaseModel):
    """A single streamed response chunk."""

    model_config = ConfigDict(
        frozen=True,
    )

    event: StreamEvent
    content: str


class StreamStart(StreamChunk):
    """Marks the beginning of a stream."""

    event: StreamEvent = StreamEvent.START
    content: str = ""


class StreamData(StreamChunk):
    """A streamed response chunk."""

    event: StreamEvent = StreamEvent.CHUNK


class StreamEnd(StreamChunk):
    """Marks the end of a stream."""

    event: StreamEvent = StreamEvent.END
    content: str = ""
