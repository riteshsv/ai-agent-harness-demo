from abc import ABC, abstractmethod
from typing import Any


class Tool(ABC):
    """
    Base class for all tools.
    The LLM will eventually see the name and description.

    The harness will invoke execute().
    """
    @property
    @abstractmethod
    def name(self) -> str:
        """
        The name of the tool.
        """
        pass

    @property
    @abstractmethod
    def description(self) -> str:
        """
        A description of the tool.
        """
        pass

    @abstractmethod
    def execute(self, *args, **kwargs:Any) -> Any:
        """
        Run the tool with the given arguments.
        """
        pass