"""Open PDF tool."""

from __future__ import annotations

import subprocess
from pathlib import Path

from tony.tools import (
    ToolArgument,
    ToolCapability,
    ToolMetadata,
    ToolResult,
)

from .base import BaseMediaTool


class OpenPdfTool(BaseMediaTool):
    """Opens a PDF using the system default application."""

    @property
    def metadata(self) -> ToolMetadata:
        return ToolMetadata(
            name="open_pdf",
            description="Open a PDF using the system default application.",
            capability=ToolCapability.FILESYSTEM,
        )

    def _execute(
        self,
        arguments: list[ToolArgument],
    ) -> ToolResult:
        """Execute the open_pdf tool."""

        if not arguments:
            return ToolResult(
                success=False,
                output="",
                error="A PDF path is required.",
            )

        pdf_path = Path(arguments[0].value)

        if not pdf_path.exists():
            return ToolResult(
                success=False,
                output="",
                error="PDF file does not exist.",
            )

        if not pdf_path.is_file():
            return ToolResult(
                success=False,
                output="",
                error="PDF path must be a file.",
            )

        file_result = subprocess.run(
            [
                "file",
                "--mime-type",
                "-b",
                str(pdf_path),
            ],
            capture_output=True,
            text=True,
            check=False,
        )

        if file_result.returncode != 0:
            return ToolResult(
                success=False,
                output="",
                error=file_result.stderr.strip(),
                exit_code=file_result.returncode,
            )

        if file_result.stdout.strip() != "application/pdf":
            return ToolResult(
                success=False,
                output="",
                error="File is not a PDF.",
                exit_code=file_result.returncode,
            )

        result = subprocess.run(
            [
                "xdg-open",
                str(pdf_path),
            ],
            capture_output=True,
            text=True,
            check=False,
        )

        return ToolResult(
            success=result.returncode == 0,
            output=result.stdout.strip(),
            error=result.stderr.strip(),
            exit_code=result.returncode,
        )