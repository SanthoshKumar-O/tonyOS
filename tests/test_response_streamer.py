from __future__ import annotations

from tony.response import (
    AnswerResponse,
)
from tony.streaming import (
    ResponseStreamer,
    StreamData,
    StreamEnd,
    StreamEvent,
    StreamStart,
)


def test_stream_response() -> None:
    streamer = ResponseStreamer()

    response = AnswerResponse(
        content="Hello from Tony!",
    )

    chunks = list(streamer.stream(response))

    assert len(chunks) == 3

    assert isinstance(chunks[0], StreamStart)
    assert chunks[0].event is StreamEvent.START

    assert isinstance(chunks[1], StreamData)
    assert chunks[1].event is StreamEvent.CHUNK
    assert chunks[1].content == "Hello from Tony!"

    assert isinstance(chunks[2], StreamEnd)
    assert chunks[2].event is StreamEvent.END


def test_stream_preserves_response_content() -> None:
    streamer = ResponseStreamer()

    response = AnswerResponse(
        content="Streaming works.",
    )

    chunks = list(streamer.stream(response))

    data = chunks[1]

    assert isinstance(data, StreamData)
    assert data.content == "Streaming works."
