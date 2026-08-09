"""Project type detection tool."""

from __future__ import annotations

from pathlib import Path

from tony.tools import (
    ToolArgument,
    ToolCapability,
    ToolMetadata,
    ToolResult,
)

from .base import BaseWorkspaceTool


class ProjectDetectTool(BaseWorkspaceTool):
    """Detect project types from workspace markers."""

    _MARKERS = {
        "pyproject.toml": "Python",
        "package.json": "Node.js",
        "Cargo.toml": "Rust",
        "go.mod": "Go",
        "pom.xml": "Java/Maven",
        "build.gradle": "Java/Gradle",
        "build.gradle.kts": "Java/Gradle",
        "CMakeLists.txt": "C/C++",
        "Makefile": "Make",
        "Dockerfile": "Docker",
        "compose.yaml": "Docker Compose",
        "docker-compose.yml": "Docker Compose",
        ".git": "Git",
    }

    @property
    def metadata(self) -> ToolMetadata:
        return ToolMetadata(
            name="project_detect",
            description="Detect project types in the current workspace.",
            capability=ToolCapability.FILESYSTEM,
        )

    def _execute(
        self,
        arguments: list[ToolArgument],
    ) -> ToolResult:
        """Detect project types."""

        current = Path.cwd().resolve()

        detected: list[str] = []

        for marker, project_type in self._MARKERS.items():
            if (current / marker).exists():
                detected.append(project_type)

        if not detected:
            return ToolResult(
                success=True,
                output="No known project types detected.",
            )

        return ToolResult(
            success=True,
            output="\n".join(detected),
        )