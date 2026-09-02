
from pathlib import Path
import subprocess
from typing import Any
from .base import Tool
from .result import ToolResult

class RunCommandTool(Tool):
    def __init__(self, workspace:Path):
            self.workspace = workspace
    
    @property
    def name(self) -> str:
        """
        The name of the tool.
        """
        return "run_command"

    @property
    def description(self) -> str:
        """
        A description of the tool.
        """
        return "Runs a shell command in the workspace."

    def execute(self, *args, **kwargs:Any) -> Any:
        """
        Run the tool with the given arguments.
        """
        try:
            command = kwargs.get("command")
        
            result = subprocess.run(
                command,
                shell=True,
                cwd=self.workspace,
                capture_output=True,
                text=True,
                timeout=30
                
            )

            return ToolResult(
                success= result.returncode == 0,
                data = {
                    "return_code":result.returncode,
                    "stdout": result.stdout,
                    "stderr": result.stderr
                }
            )
        except subprocess.TimeoutExpired:
             return ToolResult(
                success=False,
                error="Command timed out."
                )
        except Exception as ex:
            return ToolResult(
                success=False,
                error=str(ex)
                )