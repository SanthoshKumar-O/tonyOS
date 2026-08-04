"""Terminal tool registry."""

from __future__ import annotations

from tony.tools import ToolRegistry

from .cpu_info import CpuInfoTool
from .date import DateTool
from .disk_usage import DiskUsageTool
from .environment import EnvironmentTool
from .execute import ExecuteCommandTool
from .history import HistoryTool
from .hostname import HostnameTool
from .ip_address import IpAddressTool
from .kill_process import KillProcessTool
from .memory_usage import MemoryUsageTool
from .network_interfaces import NetworkInterfacesTool
from .os_info import OsInfoTool
from .ping import PingTool
from .process_list import ProcessListTool
from .uname import UnameTool
from .uptime import UptimeTool
from .which import WhichTool
from .whoami import WhoAmITool


class TerminalRegistry:
    """Registers terminal tools."""

    @staticmethod
    def register(
        registry: ToolRegistry,
    ) -> None:
        """Register terminal tools."""

        registry.register(ExecuteCommandTool())
        registry.register(ProcessListTool())
        registry.register(KillProcessTool())
        registry.register(WhoAmITool())
        registry.register(HostnameTool())
        registry.register(UnameTool())
        registry.register(DateTool())
        registry.register(UptimeTool())
        registry.register(EnvironmentTool())
        registry.register(DiskUsageTool())
        registry.register(MemoryUsageTool())
        registry.register(CpuInfoTool())
        registry.register(OsInfoTool())
        registry.register(PingTool())
        registry.register(IpAddressTool())
        registry.register(NetworkInterfacesTool())
        registry.register(WhichTool())
        registry.register(HistoryTool())
