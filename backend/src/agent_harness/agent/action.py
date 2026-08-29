from dataclasses import dataclass
from src.agent_harness.tools.base import Tool
from typing import Any

@dataclass
class AgentAction:
    """
    Contract between agent and the harness
    AgentAction(
    tool="echo",
    arguments={
        "message": "Hello from the agent"
    },
    )
    """
    tool: Tool
    arguments: dict[str,Any]
