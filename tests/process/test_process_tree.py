"""Tests for ProcessTreeTool."""

from __future__ import annotations

from unittest.mock import patch

from tony.tools.process import ProcessTreeTool


def test_metadata() -> None:
    tool = ProcessTreeTool()

    assert tool.metadata.name == "process_tree"


@patch("tony.tools.process.process_tree.subprocess.run")
def test_returns_process_tree(mock_run) -> None:
    mock_run.return_value.returncode = 0
    mock_run.return_value.stdout = (
        "1 0 root S /sbin/init\n"
        "100 1 user S python app.py\n"
        "200 100 user S worker.py\n"
    )
    mock_run.return_value.stderr = ""

    tool = ProcessTreeTool()

    result = tool.execute([])

    assert result.success is True
    assert "1 0 root" in result.output
    assert "100 1 user" in result.output
    assert "200 100 user" in result.output

    mock_run.assert_called_once_with(
        [
            "ps",
            "-eo",
            "pid=,ppid=,user=,stat=,cmd=",
            "--forest",
        ],
        capture_output=True,
        text=True,
        check=False,
    )


@patch("tony.tools.process.process_tree.subprocess.run")
def test_ps_failure(mock_run) -> None:
    mock_run.return_value.returncode = 1
    mock_run.return_value.stdout = ""
    mock_run.return_value.stderr = "ps: failed"

    tool = ProcessTreeTool()

    result = tool.execute([])

    assert result.success is False
    assert result.error == "ps: failed"
    assert result.exit_code == 1


@patch("tony.tools.process.process_tree.subprocess.run")
def test_os_error(mock_run) -> None:
    mock_run.side_effect = OSError("ps not found")

    tool = ProcessTreeTool()

    result = tool.execute([])

    assert result.success is False
    assert result.error == "ps not found"