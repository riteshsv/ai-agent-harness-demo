from abc import ABC, abstractmethod
from src.agent_harness.harness.context import AgentContext
from src.agent_harness.agent.action import AgentAction

class Agent(ABC):
    """
    Base class for all agents.
    """

    @abstractmethod
    def decide(self, context: AgentContext) -> AgentAction:
        pass