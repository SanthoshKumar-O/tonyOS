"""Tests for OpenImageTool."""

from __future__ import annotations

from pathlib import Path
from unittest.mock import patch

from tony.tools import ToolArgument
from tony.tools.media import OpenImageTool


def test_open_image_success(
    tmp_path: Path,
) -> None:
    tool = OpenImageTool()

    image = tmp_path / "test.png"
    image.write_bytes(b"fake image")

    with patch(
        "tony.tools.media.open_image.subprocess.run",
    ) as mock_run:
        mock_run.return_value.returncode = 0
        mock_run.return_value.stdout = ""
        mock_run.return_value.stderr = ""

        result = tool.execute(
            [
                ToolArgument(
                    name="path",
                    value=str(image),
                ),
            ],
        )

    assert result.success is True
    assert result.error == ""
    assert result.exit_code == 0

    mock_run.assert_called_once_with(
        [
            "xdg-open",
            str(image),
        ],
        capture_output=True,
        text=True,
        check=False,
    )


def test_open_image_without_arguments() -> None:
    tool = OpenImageTool()

    result = tool.execute([])

    assert result.success is False
    assert result.error == "An image path is required."


def test_open_image_missing_file() -> None:
    tool = OpenImageTool()

    result = tool.execute(
        [
            ToolArgument(
                name="path",
                value="/does/not/exist.png",
            ),
        ],
    )

    assert result.success is False
    assert result.error == "Image file does not exist."


def test_open_image_directory(
    tmp_path: Path,
) -> None:
    tool = OpenImageTool()

    result = tool.execute(
        [
            ToolArgument(
                name="path",
                value=str(tmp_path),
            ),
        ],
    )

    assert result.success is False
    assert result.error == "Image path must be a file."


def test_open_image_failure(
    tmp_path: Path,
) -> None:
    tool = OpenImageTool()

    image = tmp_path / "test.png"
    image.write_bytes(b"fake image")

    with patch(
        "tony.tools.media.open_image.subprocess.run",
    ) as mock_run:
        mock_run.return_value.returncode = 1
        mock_run.return_value.stdout = ""
        mock_run.return_value.stderr = "Failed to open image."

        result = tool.execute(
            [
                ToolArgument(
                    name="path",
                    value=str(image),
                ),
            ],
        )

    assert result.success is False
    assert result.error == "Failed to open image."
    assert result.exit_code == 1


def test_open_image_metadata() -> None:
    tool = OpenImageTool()

    metadata = tool.metadata

    assert metadata.name == "open_image"
    assert metadata.description == (
        "Open an image using the system default application."
    )