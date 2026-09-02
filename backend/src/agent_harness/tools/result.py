
from dataclasses import dataclass
from typing import Any


@dataclass
class ToolResult():
    """
    Represents the result of a tool execution.
    """
    success: bool
    data:Any = None
    error:str | None = None