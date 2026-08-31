from json import tool
from typing import Any
from .base import Tool

class ToolRegistry:
    """
    A registry for tools.
    The harness will use this to look up tools by name.
                      Tool Registry
                       │
          ┌────────────┼────────────┐
          ▼            ▼            ▼
      read_file    write_file   run_command

    Later the harness can expose the registry to the agent
    
    """
    def __init__(self):
        self._tools : dict[str,Any] = {}

    def register_tool(self, tool: Tool):
        self._tools[tool.name] = tool

    def get(self, tool_name:str) -> Tool | None:
        if tool_name not in self._tools:
            raise ValueError(f"Tool {tool_name} not found in registry")
        return self._tools.get(tool_name)

    def list_tools(self) -> list[str]:
        return list(self._tools.keys())

    def describe_tools(self) -> dict[str,str]:
        return [
            {
                "name": tool.name,
                "description": tool.description
            } 
            for tool in self._tools.values()
        ]