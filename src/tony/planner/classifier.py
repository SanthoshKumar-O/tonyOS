"""Intent classifier."""

from __future__ import annotations

from tony.context import ExecutionContext
from tony.planner.models import PlanType


class IntentClassifier:
    """Classifies the user's intent."""

    _EXECUTE_KEYWORDS = {
        "delete",
        "remove",
        "rm",
        "mkdir",
        "touch",
        "mv",
        "cp",
        "git",
        "clone",
        "commit",
        "push",
        "pull",
        "install",
        "pip",
        "uv",
        "cargo",
        "docker",
        "systemctl",
        "dnf",
        "apt",
    }

    _CLARIFY_KEYWORDS = {
        "which",
        "what repository",
        "what repo",
        "which repository",
        "which repo",
        "what folder",
        "which folder",
        "which project",
        "what project",
    }

    def classify(
        self,
        context: ExecutionContext,
    ) -> PlanType:
        """Determine the appropriate plan type."""

        message = context.conversation.last_message()

        if message is None:
            return PlanType.ANSWER

        text = message.content.lower()

        if any(keyword in text for keyword in self._CLARIFY_KEYWORDS):
            return PlanType.CLARIFY

        if any(keyword in text for keyword in self._EXECUTE_KEYWORDS):
            return PlanType.EXECUTE

        return PlanType.ANSWER
