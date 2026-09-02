from src.agent_harness.harness.events import emit
from src.agent_harness.tools.registry import ToolRegistry
from .context import AgentContext
from .state import AgentState
from src.agent_harness.agent.action import AgentAction
from ..tools.result import ToolResult

class AgentHarness:
    def __init__(self, goal: str, tools: ToolRegistry):
        """
        The harness is the orchestrator of the agent's reasoning process.
                Agent Harness
                      │
          ┌───────────┼───────────┐
          │           │           │
          ▼           ▼           ▼
        State       Context      Tools
          │                       │
          │                 Tool Registry
          │                       │
          └───────────┬───────────┘
                      ▼
                   Events
                      │
                      ▼
                  React Ink

        The harness is responsible for:
        Maintain state
        harness.state
        Create agent context
        harness.create_context()
        Record observations
        harness.observe(...)
        Execute tools
        harness.execute_tool(...)
        Emit events
        observation
        tool_started
        tool_completed
        """
        self.tools : ToolRegistry = tools
        self.state = AgentState(goal=goal)

    def create_context(self) -> AgentContext:
        """
        Create a context for the agent to reason about.
        """
        return AgentContext(
            state=self.state, 
            available_tools=self.tools.describe_tools()
            )
    def observe(self, observation: str):
        """
        Add an observation to the state.
        """
        self.state.observations.append(observation)
        emit(
            "observation",
            content=observation
            )
    def execute_action(
        self,
        action: AgentAction
    ):
        """
        Execute an action and add the result to the state.
        """
        return self.execute_tool(
            action.tool,
            action.arguments
        )
    def execute_tool(
            self,
            tool_name:str,
            arguments: dict
            ) -> ToolResult:
        """
        Execute a tool and add the result to the state.
        """
        emit(
            "tool_started",
            tool=tool_name,
            arguments=arguments
        )
        try:

            tool = self.tools.get(tool_name)
            result = tool.execute(**arguments)
        except Exception as e:
            result = ToolResult(
                success=False,
                error=str(e)
            )
        self.state.actions.append(
            {
                "tool": tool_name, 
                "arguments": arguments
                }
                )
        self.state.last_result = result
        emit(
            "tool_completed",
            tool=tool_name,
            success=result.success,
            data=result.data if result.success else None,
            error=result.error if not result.success else None
        )
        return result