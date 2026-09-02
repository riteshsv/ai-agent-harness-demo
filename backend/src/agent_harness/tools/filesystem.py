from pathlib import Path
from typing import Any
from .base import Tool
from .result import ToolResult

def resolve_workspace_path(
        workspace:Path,
        relative_path:str
):
    workspace = workspace.resolve()
    target_path = (workspace / relative_path).resolve()
    if not target_path.is_relative_to(workspace):
        raise ValueError(f"Path {relative_path} is outside the workspace.")
    return target_path


class ReadTool(Tool):
    def __init__(self, workspace:Path):
        self.workspace = workspace

    @property
    def name(self) -> str:
        """
        The name of the tool.
        """
        return "read_file"

    @property
    def description(self) -> str:
        """
        A description of the tool.
        """
        return "Reads the content of a file in the workspace."

    def execute(self, *args, **kwargs:Any) -> Any:
        """
        Run the tool with the given arguments.
        """
        try:
            path = kwargs.get("path")
            if path is None:
                return ToolResult(
                    success=False,
                    error="Path argument is required."
                    )
            resolved_path = resolve_workspace_path(self.workspace, path)
            if not resolved_path.exists():
                return ToolResult(
                    success=False,
                    error=f"File {path} does not exist."
                )
                
            content = resolved_path.read_text()

            return ToolResult(
                success=True,
                data={
                    "path":path,
                    "content": content
                } 
            )
        except Exception as ex:
            return ToolResult(
                success=False,
                error=str(ex)
            )
        

class WriteTool(Tool):
    def __init__(self, workspace:Path):
        self.workspace = workspace

    @property
    def name(self) -> str:
        """
        The name of the tool.
        """
        return "write_file"

    @property
    def description(self) -> str:
        """
        A description of the tool.
        """
        return "Writes content to a file in the workspace."

    def execute(self, *args, **kwargs:Any) -> Any:
        """
        Run the tool with the given arguments.
        """
        try:
            path = kwargs.get("path")
            content = kwargs.get("content")

            if path is None:
                return ToolResult(
                    success=False,
                    error="Path argument is required."
                )

            resolved_path = resolve_workspace_path(self.workspace, path)
            if not resolved_path.exists():
                return ToolResult(
                    success=False,
                    error=f"File {path} does not exist."
                )

            resolved_path.parent.mkdir(
                parents=True, 
                exist_ok=True
            )
            resolved_path.write_text(content)

            return ToolResult(
                    success=True,
                    data = {
                        "path":path
                        }
                    )
        except Exception as ex:
            return ToolResult(
                success=False,
                error=str(ex)
            )
