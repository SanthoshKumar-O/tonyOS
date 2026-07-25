from tony.tools import ToolArgument
from tony.tools.shell import ShellTool

tool = ShellTool()

result = tool.execute(
    [
        ToolArgument(name="command", value="ls"),
        ToolArgument(name="arg1", value="/this/path/does/not/exist"),
    ]
)

print(result)
