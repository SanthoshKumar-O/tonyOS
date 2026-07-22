"""Response models."""

from __future__ import annotations

from enum import StrEnum

from pydantic import BaseModel, ConfigDict


class ResponseType(StrEnum):
    """Supported response types."""

    ANSWER = "answer"
    CLARIFICATION = "clarification"
    EXECUTION = "execution"


class Response(BaseModel):
    """Base response returned by Tony."""

    model_config = ConfigDict(
        frozen=True,
    )

    response_type: ResponseType
    content: str


class AnswerResponse(Response):
    """Response containing an answer."""

    response_type: ResponseType = ResponseType.ANSWER


class ClarificationResponse(Response):
    """Response requesting clarification."""

    response_type: ResponseType = ResponseType.CLARIFICATION


class ExecutionResponse(Response):
    """Response describing an execution."""

    response_type: ResponseType = ResponseType.EXECUTION
