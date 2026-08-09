"""Tests for the process tool registry."""

from __future__ import annotations

from tony.tools import ToolRegistry
from tony.tools.process import register_process_tools


EXPECTED_TOOLS = {
    "process_affinity",
    "process_children",
    "process_cgroup",
    "process_command_line",
    "process_cpu_times",
    "process_environment",
    "process_executable",
    "process_fds",
    "process_file_descriptors",
    "process_identity",
    "inspect_process",
    "process_io",
    "process_limits",
    "process_maps",
    "process_namespaces",
    "process_open_files",
    "process_signal",
    "process_tree",
    "process_resource_usage",
    "process_root_directory",
    "process_sched",
    "process_scheduler",
    "process_session",
    "set_process_priority",
    "process_stats",
    "process_status",
    "process_status_flags",
    "process_threads",
    "process_working_directory",
}


def test_register_process_tools() -> None:
    registry = ToolRegistry()

    register_process_tools(registry)

    registered_names = {
        tool.metadata.name
        for tool in registry.tools()
    }

    assert registered_names == EXPECTED_TOOLS


def test_register_process_tools_count() -> None:
    registry = ToolRegistry()

    register_process_tools(registry)

    assert len(registry.tools()) == 29