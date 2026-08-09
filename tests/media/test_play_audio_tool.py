"""Tests for PlayAudioTool."""

from __future__ import annotations

from pathlib import Path
from unittest.mock import patch

from tony.tools import ToolArgument
from tony.tools.media import PlayAudioTool


def test_play_audio_success(
    tmp_path: Path,
) -> None:
    tool = PlayAudioTool()

    audio = tmp_path / "test.mp3"
    audio.write_bytes(b"fake audio")

    with patch(
        "tony.tools.media.play_audio.subprocess.run",
    ) as mock_run:
        mock_run.return_value.returncode = 0
        mock_run.return_value.stdout = ""
        mock_run.return_value.stderr = ""

        result = tool.execute(
            [
                ToolArgument(
                    name="path",
                    value=str(audio),
                ),
            ],
        )

    assert result.success is True
    assert result.error == ""
    assert result.exit_code == 0

    mock_run.assert_called_once_with(
        [
            "xdg-open",
            str(audio),
        ],
        capture_output=True,
        text=True,
        check=False,
    )


def test_play_audio_without_arguments() -> None:
    tool = PlayAudioTool()

    result = tool.execute([])

    assert result.success is False
    assert result.error == "An audio path is required."


def test_play_audio_missing_file() -> None:
    tool = PlayAudioTool()

    result = tool.execute(
        [
            ToolArgument(
                name="path",
                value="/does/not/exist.mp3",
            ),
        ],
    )

    assert result.success is False
    assert result.error == "Audio file does not exist."


def test_play_audio_directory(
    tmp_path: Path,
) -> None:
    tool = PlayAudioTool()

    result = tool.execute(
        [
            ToolArgument(
                name="path",
                value=str(tmp_path),
            ),
        ],
    )

    assert result.success is False
    assert result.error == "Audio path must be a file."


def test_play_audio_failure(
    tmp_path: Path,
) -> None:
    tool = PlayAudioTool()

    audio = tmp_path / "test.mp3"
    audio.write_bytes(b"fake audio")

    with patch(
        "tony.tools.media.play_audio.subprocess.run",
    ) as mock_run:
        mock_run.return_value.returncode = 1
        mock_run.return_value.stdout = ""
        mock_run.return_value.stderr = "Failed to play audio."

        result = tool.execute(
            [
                ToolArgument(
                    name="path",
                    value=str(audio),
                ),
            ],
        )

    assert result.success is False
    assert result.error == "Failed to play audio."
    assert result.exit_code == 1


def test_play_audio_metadata() -> None:
    tool = PlayAudioTool()

    metadata = tool.metadata

    assert metadata.name == "play_audio"
    assert metadata.description == (
        "Play an audio file using the system default application."
    )