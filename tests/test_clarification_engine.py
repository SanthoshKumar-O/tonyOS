from __future__ import annotations

from tony.clarification import (
    ClarificationEngine,
    ClarificationRequest,
)
from tony.planner import (
    ClarificationPlan,
)


def test_generate_clarification_request() -> None:
    engine = ClarificationEngine()

    plan = ClarificationPlan(
        reason="Which repository would you like to use?",
        confidence=0.95,
    )

    request = engine.generate(
        plan,
    )

    assert isinstance(
        request,
        ClarificationRequest,
    )

    assert request.question == "Which repository would you like to use?"
