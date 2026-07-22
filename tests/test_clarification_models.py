from __future__ import annotations

import pytest
from pydantic import ValidationError

from tony.clarification import (
    ClarificationRequest,
)


def test_clarification_request() -> None:
    request = ClarificationRequest(
        question="Which repository?",
    )

    assert request.question == "Which repository?"


def test_model_is_immutable() -> None:
    request = ClarificationRequest(
        question="Which repository?",
    )

    with pytest.raises(ValidationError):
        request.question = "Changed"
