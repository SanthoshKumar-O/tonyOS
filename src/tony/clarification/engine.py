"""Clarification engine."""

from __future__ import annotations

from tony.planner import ClarificationPlan

from .models import ClarificationRequest


class ClarificationEngine:
    """Builds clarification requests from clarification plans."""

    def generate(
        self,
        plan: ClarificationPlan,
    ) -> ClarificationRequest:
        """Generate a clarification request."""

        return ClarificationRequest(
            question=plan.reason,
        )
