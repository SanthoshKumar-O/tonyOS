"""Tests for OpenPdfTool."""

from __future__ import annotations

from pathlib import Path
from unittest.mock import patch

from tony.tools import ToolArgument
from tony.tools.media import OpenPdfTool


def test_open_pdf_success(
    tmp_path: Path,
) -> None:
    tool = OpenPdfTool()

    pdf = tmp_path / "test.pdf"
    pdf.write_bytes(b"%PDF-1.7")

    with patch(
        "tony.tools.media.open_pdf.subprocess.run",
    ) as mock_run:
        mock_run.side_effect = [
            type(
                "Result",
                (),
                {
                    "returncode": 0,
                    "stdout": "application/pdf\n",
                    "stderr": "",
                },
            )(),
            type(
                "Result",
                (),
                {
                    "returncode": 0,
                    "stdout": "",
                    "stderr": "",
                },
            )(),
        ]

        result = tool.execute(
            [
                ToolArgument(
                    name="path",
                    value=str(pdf),
                ),
            ],
        )

    assert result.success is True
    assert result.error == ""
    assert result.exit_code == 0
    assert mock_run.call_count == 2


def test_open_pdf_without_arguments() -> None:
    tool = OpenPdfTool()

    result = tool.execute([])

    assert result.success is False
    assert result.error == "A PDF path is required."


def test_open_pdf_missing_file() -> None:
    tool = OpenPdfTool()

    result = tool.execute(
        [
            ToolArgument(
                name="path",
                value="/does/not/exist.pdf",
            ),
        ],
    )

    assert result.success is False
    assert result.error == "PDF file does not exist."


def test_open_pdf_directory(
    tmp_path: Path,
) -> None:
    tool = OpenPdfTool()

    result = tool.execute(
        [
            ToolArgument(
                name="path",
                value=str(tmp_path),
            ),
        ],
    )

    assert result.success is False
    assert result.error == "PDF path must be a file."


def test_open_pdf_unsupported_file(
    tmp_path: Path,
) -> None:
    tool = OpenPdfTool()

    text_file = tmp_path / "test.txt"
    text_file.write_text(
        "not a PDF",
        encoding="utf-8",
    )

    with patch(
        "tony.tools.media.open_pdf.subprocess.run",
    ) as mock_run:
        mock_run.return_value.returncode = 0
        mock_run.return_value.stdout = "text/plain\n"
        mock_run.return_value.stderr = ""

        result = tool.execute(
            [
                ToolArgument(
                    name="path",
                    value=str(text_file),
                ),
            ],
        )

    assert result.success is False
    assert result.error == "File is not a PDF."


def test_open_pdf_failure(
    tmp_path: Path,
) -> None:
    tool = OpenPdfTool()

    pdf = tmp_path / "test.pdf"
    pdf.write_bytes(b"%PDF-1.7")

    with patch(
        "tony.tools.media.open_pdf.subprocess.run",
    ) as mock_run:
        mock_run.side_effect = [
            type(
                "Result",
                (),
                {
                    "returncode": 0,
                    "stdout": "application/pdf\n",
                    "stderr": "",
                },
            )(),
            type(
                "Result",
                (),
                {
                    "returncode": 1,
                    "stdout": "",
                    "stderr": "Failed to open PDF.",
                },
            )(),
        ]

        result = tool.execute(
            [
                ToolArgument(
                    name="path",
                    value=str(pdf),
                ),
            ],
        )

    assert result.success is False
    assert result.error == "Failed to open PDF."
    assert result.exit_code == 1


def test_open_pdf_metadata() -> None:
    tool = OpenPdfTool()

    metadata = tool.metadata

    assert metadata.name == "open_pdf"
    assert metadata.description == (
        "Open a PDF using the system default application."
    )