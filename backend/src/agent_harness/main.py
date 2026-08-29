
from src.agent_harness.harness.harness import AgentHarness
from src.agent_harness.harness.events import emit
from src.agent_harness.tools.base import Tool
from src.agent_harness.tools.registry import ToolRegistry

class EchoTool(Tool):
    @property
    def name(self) -> str:
        return "echo"

    @property
    def description(self) -> str:
        return "Echoes the input back to the user."

    def execute(self, *args, **kwargs):
        """
        Echoes the input back to the user.
        """
        # handle all kwargs
        message = kwargs.get("message", "")
        if not message:
            raise ValueError("No message provided to echo.")
        return message

def main():

    emit(
        "backend_started",
        message="Harness started successfully."
    )
    
    registry = ToolRegistry()
    registry.register_tool(EchoTool())

    harness = AgentHarness(
        "Demo use of Echo Tool",
        registry
    )

    harness.observe("Starting the harness with Echo Tool.")
    context = harness.create_context()

    harness.execute_tool(
        "echo",
        {
            "message":"Hello, Echo Tool!"
        }
    )



if __name__ == "__main__":
    main()
