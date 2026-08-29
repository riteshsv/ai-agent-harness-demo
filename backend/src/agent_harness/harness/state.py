# document the code in this file

# The state belongs to the harness, not the LLM.

# The LLM may reason about the state, but the harness owns it.

# That's an important architectural principle.

# goal:
#     "Create a Fibonacci function"

# iteration:
#     2

# status:
#     "running"

# observations:
#     [
#         "solution.py is empty",
#         "pytest failed: expected 5, got 4"
#     ]

# actions:
#     [
#         {"tool": "write_file"},
#         {"tool": "run_command"}
#     ]

# last_result:
#     "pytest passed"
from dataclasses import dataclass,field
from typing import Any


@dataclass
class AgentState:
    goal: str = ""
    iteration: int = 0
    status: str = "running"

    observations: list[str] = field(default_factory=list)
    actions: list[dict[str,Any]] = field(default_factory=list)

    last_result: Any = None
