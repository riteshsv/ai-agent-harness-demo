from pathlib import Path
from typing import Any
from .base import Tool

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
        path = kwargs.get("path")
        if path is None:
            raise ValueError("Path argument is required.")
        resolved_path = resolve_workspace_path(self.workspace, path)
        print(f"Resolved path: {resolved_path}")
        if not resolved_path.exists():
            return {
                "success": False,
                "error": f"File {path} does not exist."
            }
        content = resolved_path.read_text()

        return {
            "success": True,
            "path":path,
            "content": content
        }

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
        path = kwargs.get("path")
        content = kwargs.get("content")

        if path is None:
            raise ValueError("Path argument is required.")

        resolved_path = resolve_workspace_path(self.workspace, path)
        if not resolved_path.exists():
            return {
                "success": False,
                "error": f"File {path} does not exist."
            }

        resolved_path.parent.mkdir(
            parents=True, 
            exist_ok=True
        )
        resolved_path.write_text(content)

        return {
            "success": True,
            "path":path
            
        }
