
from pathlib import Path
import subprocess
from typing import Any
from .base import Tool


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
        command = kwargs.get("command")
       
        result = subprocess.run(
            command,
            shell=True,
            cwd=self.workspace,
            capture_output=True,
            text=True,
            timeout=30
            
        )

        return {
            "success": result.returncode == 0,
            "return_code":result.returncode,
            "stdout": result.stdout,
            "stderr": result.stderr
        }