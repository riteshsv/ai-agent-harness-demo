from dataclasses import dataclass
from .state import AgentState


@dataclass
class AgentContext:
    """
    The context is a read-only view of the state.

    The LLM can reason about the context, but it cannot modify it.

    That's an important architectural principle.
    This represents the information we provide to the agent for a particular decision.

    State
    │
    ▼
    Context
    │
    ├── Goal
    ├── Iteration
    ├── Observations
    ├── Previous actions
    └── Available tools
            │
            ▼
            Agent
    Later, the context will become the input to the LLM.
    """
    state: AgentState
    available_tools: list[str]