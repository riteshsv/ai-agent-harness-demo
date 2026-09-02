
from pathlib import Path
from .tools.filesystem import ReadTool, WriteTool
from .tools.shell import RunCommandTool
from src.agent_harness.loop.ralph import RalphLoop
from src.agent_harness.agent.mock_agent import MockAgent
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
        return {
            "message":message,
            "success":True
        }

def main():

    #start the harness

    emit(
        "backend_started",
        message="Harness started successfully."
    )
    workspace = Path("../workspace").resolve()

    #--------------------
    # Create Tools
    #--------------------
    
    registry = ToolRegistry()
    registry.register_tool(EchoTool())
    registry.register_tool(ReadTool(workspace))
    registry.register_tool(WriteTool(workspace))
    registry.register_tool(RunCommandTool(workspace))
    #--------------------
    # Start the Harness
    #--------------------

    harness = AgentHarness(
        "Pytest return code 0",
        registry
    )

    # ------------------
    # Create Agent
    # ------------------

    agent = MockAgent()

    # --------------------
    # Observe Environment
    # --------------------


    harness.observe("The workspace is ready")
    
    # ----------------------
    # Ralph loop
    # ----------------------
    loop = RalphLoop(
        agent=agent,
        harness=harness,
        max_iterations=3
    )

    loop.run()



if __name__ == "__main__":
    main()
