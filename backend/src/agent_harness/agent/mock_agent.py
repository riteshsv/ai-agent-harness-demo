from src.agent_harness.harness.context import AgentContext
from src.agent_harness.agent.base import Agent
from src.agent_harness.agent.action import AgentAction
class MockAgent(Agent):
    def decide(self,context: AgentContext) -> AgentAction:
        """
        A mock agent that always returns a fixed action.
        """

        return AgentAction(
            tool="read_file",
            arguments={
                "path": "task.md"
            }
        )