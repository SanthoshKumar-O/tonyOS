from typing import Protocol

from tony.context import ExecutionContext
from tony.context_builder.models import PromptBuildResult


class ContextBuilderProtocol(Protocol):
    def build(
        self,
        context: ExecutionContext,
    ) -> PromptBuildResult: ...
