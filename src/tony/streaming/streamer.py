"""Response streamer."""

from __future__ import annotations

from collections.abc import Iterator

from tony.response import Response

from .models import (
    StreamData,
    StreamEnd,
    StreamStart,
)


class ResponseStreamer:
    """Streams response objects."""

    def stream(
        self,
        response: Response,
    ) -> Iterator[StreamStart | StreamData | StreamEnd]:
        """Convert a response into a stream."""

        yield StreamStart()

        yield StreamData(
            content=response.content,
        )

        yield StreamEnd()
