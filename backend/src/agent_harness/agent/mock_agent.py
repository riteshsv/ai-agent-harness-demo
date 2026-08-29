from src.agent_harness.harness.context import AgentContext
from src.agent_harness.agent.base import Agent
from src.agent_harness.agent.action import AgentAction
class MockAgent(Agent):
    def decide(self,context: AgentContext) -> AgentAction:
        """
        A mock agent that always returns a fixed action.
        """

        if "echo" not in context.available_tools:
            raise RuntimeError("Echo tool is not available in the context.")
        return AgentAction(
            tool="echo",
            arguments={
                "message": (
                    f"Iteration {context.state.iteration}: "
                    "Hello from the agent!"
                )
            }
        )