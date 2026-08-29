
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
        return message

def main():

    #start the harness

    emit(
        "backend_started",
        message="Harness started successfully."
    )

    #--------------------
    # Create Tools
    #--------------------
    
    registry = ToolRegistry()
    registry.register_tool(EchoTool())

    #--------------------
    # Start the Harness
    #--------------------

    harness = AgentHarness(
        "Demo use of Echo Tool",
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
    # Create the Context
    # ----------------------
    context = harness.create_context()

    # ---------------------
    # Agent decides what to do
    # -------------------

    action = agent.decide(context)

    # ----------------------------
    # harness executes the action 
    # ----------------------------

    harness.execute_action(action)

    # harness.execute_tool(
    #     "echo",
    #     {
    #         "message":"Hello, Echo Tool!"
    #     }
    # )



if __name__ == "__main__":
    main()
