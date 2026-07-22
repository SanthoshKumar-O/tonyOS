from __future__ import annotations

import pytest
from pydantic import ValidationError

from tony.streaming import (
    StreamChunk,
    StreamData,
    StreamEnd,
    StreamEvent,
    StreamStart,
)


def test_stream_chunk() -> None:
    chunk = StreamChunk(
        event=StreamEvent.CHUNK,
        content="Hello",
    )

    assert chunk.event is StreamEvent.CHUNK
    assert chunk.content == "Hello"


def test_stream_start() -> None:
    chunk = StreamStart()

    assert chunk.event is StreamEvent.START
    assert chunk.content == ""


def test_stream_data() -> None:
    chunk = StreamData(
        content="Tony",
    )

    assert chunk.event is StreamEvent.CHUNK
    assert chunk.content == "Tony"


def test_stream_end() -> None:
    chunk = StreamEnd()

    assert chunk.event is StreamEvent.END
    assert chunk.content == ""


def test_models_are_immutable() -> None:
    chunk = StreamData(
        content="Immutable",
    )

    with pytest.raises(ValidationError):
        chunk.content = "Changed"
