"""Tool selection for execution plans."""

from __future__ import annotations

from typing import Protocol

from tony.context import ExecutionContext
from tony.planner.exceptions import PlanningError
from tony.tools import ToolSelection


class ToolSelectorProtocol(Protocol):
    """Tool selector interface."""

    def select(
        self,
        context: ExecutionContext,
    ) -> ToolSelection: ...


class ToolSelector:
    """Selects a concrete tool for an execution request."""

    _TOOL_KEYWORDS: dict[str, tuple[str, ...]] = {
        "git_status": ("git status",),
        "git_clone": ("git clone",),
        "git_add": ("git add",),
        "git_commit": ("git commit",),
        "git_branch": ("git branch",),
        "git_checkout": ("git checkout",),
        "git_log": ("git log",),
        "git_diff": ("git diff",),
        "git_init": ("git init",),
        "mkdir": ("mkdir", "create directory", "make directory"),
        "touch": ("touch", "create file"),
        "rm": ("rm", "remove file", "delete file"),
        "mv": ("mv", "move file"),
        "cp": ("cp", "copy file"),
        "ls": ("ls", "list directory", "list files"),
        "pwd": ("pwd", "current working directory"),
    }

    def __init__(self, tool_registry) -> None:
        self._tool_registry = tool_registry

    def select(self, context: ExecutionContext) -> ToolSelection:
        """Select a concrete tool from the user request."""

        message = context.conversation.last_message()

        if message is None:
            raise PlanningError("Cannot select a tool without a user message.")

        text = message.content.lower()

        for tool_name, keywords in self._TOOL_KEYWORDS.items():
            if not self._tool_registry.exists(tool_name):
                continue

            if any(keyword in text for keyword in keywords):
                return ToolSelection(
                    tool_name=tool_name,
                    confidence=1.0,
                    reason=f"Selected tool '{tool_name}' from the execution request.",
                )

        raise PlanningError(
            "Unable to determine a concrete tool for the execution request.",
        )