from __future__ import annotations

from pathlib import Path

from tony.execution.service import ExecutionService
from tony.tools import (
    ArgumentValidator,
    PermissionEngine,
    ToolArgument,
    ToolDiscovery,
    ToolDispatcher,
    ToolRegistry,
    ToolSelection,
)
from tony.tools.filesystem.registry import register_filesystem_tools
from tony.tools.git import GitRegistry


def create_service() -> tuple[
    ToolRegistry,
    ToolDiscovery,
    ExecutionService,
]:
    registry = ToolRegistry()

    register_filesystem_tools(registry)
    GitRegistry.register(registry)

    discovery = ToolDiscovery(registry)

    service = ExecutionService(
        permission_engine=PermissionEngine(registry),
        argument_validator=ArgumentValidator(),
        dispatcher=ToolDispatcher(registry),
    )

    return registry, discovery, service


def test_filesystem_and_git_workflow(
    tmp_path: Path,
) -> None:
    _, _, service = create_service()

    mkdir = ToolSelection(
        tool_name="mkdir",
        confidence=1.0,
        reason="Create test workspace.",
    )

    result = service.execute(
        mkdir,
        [
            ToolArgument(
                name="path",
                value=str(tmp_path / "workspace"),
            ),
        ],
    )

    assert result.success is True
    assert (tmp_path / "workspace").is_dir()

    touch = ToolSelection(
        tool_name="touch",
        confidence=1.0,
        reason="Create README file.",
    )

    result = service.execute(
        touch,
        [
            ToolArgument(
                name="path",
                value=str(tmp_path / "workspace" / "README.md"),
            ),
        ],
    )

    assert result.success is True
    assert (tmp_path / "workspace" / "README.md").is_file()

    ls = ToolSelection(
        tool_name="ls",
        confidence=1.0,
        reason="List workspace contents.",
    )

    result = service.execute(
        ls,
        [
            ToolArgument(
                name="path",
                value=str(tmp_path / "workspace"),
            ),
        ],
    )

    assert result.success is True
    assert "README.md" in result.output

    git_init = ToolSelection(
        tool_name="git_init",
        confidence=1.0,
        reason="Initialize Git repository.",
    )

    result = service.execute(
        git_init,
        [
            ToolArgument(
                name="path",
                value=str(tmp_path / "workspace"),
            ),
        ],
    )

    assert result.success is True
    assert (tmp_path / "workspace" / ".git").is_dir()

    git_status = ToolSelection(
        tool_name="git_status",
        confidence=1.0,
        reason="Check Git repository status.",
    )

    result = service.execute(
        git_status,
        [
            ToolArgument(
                name="path",
                value=str(tmp_path / "workspace"),
            ),
        ],
    )

    assert result.success is True
