"""Process tool registry."""

from __future__ import annotations

from tony.tools import ToolRegistry

from .affinity import ProcessAffinityTool
from .cgroup import ProcessCgroupTool
from .command_line import ProcessCommandLineTool
from .environment import ProcessEnvironmentTool
from .executable import ProcessExecutableTool
from .fds import ProcessFdsTool
from .file_descriptors import ProcessFileDescriptorsTool
from .inspect_process import InspectProcessTool
from .io import ProcessIOTool
from .limits import ProcessLimitsTool
from .maps import ProcessMapsTool
from .namespaces import ProcessNamespacesTool
from .open_files import ProcessOpenFilesTool
from .process_tree import ProcessTreeTool
from .resource_usage import ProcessResourceUsageTool
from .root_directory import ProcessRootDirectoryTool
from .sched import ProcessSchedTool
from .scheduler import ProcessSchedulerTool
from .set_priority import SetProcessPriorityTool
from .status import ProcessStatusTool
from .status_flags import ProcessStatusFlagsTool
from .threads import ProcessThreadsTool
from .working_directory import ProcessWorkingDirectoryTool
from .process_signal import ProcessSignalTool
from .children import ProcessChildrenTool
from .identity import ProcessIdentityTool
from .session import ProcessSessionTool
from .cpu_times import ProcessCpuTimesTool
from .stats import ProcessStatsTool


def register_process_tools(
    registry: ToolRegistry,
) -> None:
    """Register all process management tools."""

    registry.register(ProcessAffinityTool())
    registry.register(ProcessChildrenTool())
    registry.register(ProcessCgroupTool())
    registry.register(ProcessCommandLineTool())
    registry.register(ProcessCpuTimesTool())
    registry.register(ProcessEnvironmentTool())
    registry.register(ProcessExecutableTool())
    registry.register(ProcessFdsTool())
    registry.register(ProcessFileDescriptorsTool())
    registry.register(ProcessIdentityTool())
    registry.register(InspectProcessTool())
    registry.register(ProcessIOTool())
    registry.register(ProcessLimitsTool())
    registry.register(ProcessMapsTool())
    registry.register(ProcessNamespacesTool())
    registry.register(ProcessOpenFilesTool())
    registry.register(ProcessSignalTool())
    registry.register(ProcessTreeTool())
    registry.register(ProcessResourceUsageTool())
    registry.register(ProcessRootDirectoryTool())
    registry.register(ProcessSchedTool())
    registry.register(ProcessSchedulerTool())
    registry.register(ProcessSessionTool())
    registry.register(SetProcessPriorityTool())
    registry.register(ProcessStatsTool())
    registry.register(ProcessStatusTool())
    registry.register(ProcessStatusFlagsTool())
    registry.register(ProcessThreadsTool())
    registry.register(ProcessWorkingDirectoryTool())