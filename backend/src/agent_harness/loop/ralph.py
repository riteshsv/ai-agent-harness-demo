from dataclasses import asdict

from ..tools.result import ToolResult

from ..agent.base import Agent
from ..harness.harness import AgentHarness
from ..harness.events import emit

class RalphLoop:
    """
    The RalphLoop is the orchestrator of the agent's reasoning process.
    
    """
    def __init__(
        self,
        agent,
        harness,
        max_iterations=3
        ):
        self.agent: Agent = agent
        self.harness: AgentHarness = harness
        self.max_iterations: int = max_iterations

    def run(self) -> None:

        #iterations
        for iteration in range(1,self.max_iterations+1):
            self.harness.state.iteration = iteration            #update state with iteration

            emit(
                "iteration_started",
                iteration=iteration
            )

            #create context
            if iteration == 1:
                context = self.harness.create_context()

            #decide
            action = self.agent.decide(context)

            emit(
                "agent_decision",
                tool=action.tool,
                arguments=action.arguments
            )
            

            #execute
            result = self.harness.execute_action(action)
            self.harness.state.last_result = {
                "tool": action.tool,
                "arguments": action.arguments,
                "result": asdict(result)
            } #update state with last result
            #evaluate

            if isinstance(result,ToolResult) and result.success:
                goal = self.harness.state.goal
                if goal == f"Pytest return code {result.data.get("return_code")}":
                    self.harness.state.goal_achieved = True
                
                

            if self.harness.state.goal_achieved:
                self.harness.state.status = "completed"
                emit(
                    "goal_achieved",
                    iterations=iteration,
                    
                )
                # observe
                self.harness.observe(f"Action: {action.description} success: {result.success}")
                self.harness.observe("Goal achieved. Exiting loop.")
                break

            
            # goal not achieved so contitue iteration    
            emit(
                "iteration_completed",
                iteration=iteration,
                result=asdict(result)
                )
            # observe
            self.harness.observe(f"Action: {action.description} success: {result.success}")

