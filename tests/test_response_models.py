from __future__ import annotations

import pytest
from pydantic import ValidationError

from tony.response import (
    AnswerResponse,
    ClarificationResponse,
    ExecutionResponse,
    Response,
    ResponseType,
)


def test_response() -> None:
    response = Response(
        response_type=ResponseType.ANSWER,
        content="Hello",
    )

    assert response.response_type is ResponseType.ANSWER
    assert response.content == "Hello"


def test_answer_response() -> None:
    response = AnswerResponse(
        content="Tony here.",
    )

    assert response.response_type is ResponseType.ANSWER


def test_clarification_response() -> None:
    response = ClarificationResponse(
        content="Which repository?",
    )

    assert response.response_type is ResponseType.CLARIFICATION


def test_execution_response() -> None:
    response = ExecutionResponse(
        content="Executing command...",
    )

    assert response.response_type is ResponseType.EXECUTION


def test_models_are_immutable() -> None:
    response = AnswerResponse(
        content="Immutable",
    )

    with pytest.raises(ValidationError):
        response.content = "Changed"
