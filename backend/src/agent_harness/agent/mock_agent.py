import textwrap
from tkinter import N

from ..harness.context import AgentContext
from ..agent.base import Agent
from ..agent.action import AgentAction


class MockAgent(Agent):
    def decide(self, context: AgentContext) -> AgentAction:
        """
        A mock agent that always returns a fixed action.
        """

        # read file task.md

        state = context.state
        latest_task_entry = None
        for obs in reversed(state.observations):
            if "task.md" in obs:
                latest_task_entry = obs
                break
        if latest_task_entry:
            if 'success: False' in latest_task_entry:
                # If the file has not been read, read it
                return AgentAction(
                    tool="read_file",
                    arguments={
                        "path": "task.md"
                    },
                    description="Read the task description from task.md"
                )
        else:
            # If the file has not been read, read it
            return AgentAction(
                tool="read_file",
                arguments={
                    "path": "task.md"
                },
                description="Read the task description from task.md"
            )

        latest_solution_entry = None
        for obs in reversed(state.observations):
            if "solution.py" in obs:
                latest_solution_entry = obs
                break
        if latest_solution_entry:
            # If the file has not been written, write it
            if 'success: False' in latest_solution_entry:
                return AgentAction(
                    tool="write_file",
                    arguments={
                        "path": "solution.py",
                        "content": textwrap.dedent("""\
                            def fibonacci_fast(n):
                                if n <= 1:
                                    return n
                                
                                a, b = 0, 1
                                for _ in range(2, n + 1):
                                    a, b = b, a + b
                                return b""")
                    },
                    description="Write the Fibonacci function to solution.py"
                )
        else:
            # If the file has not been written, write it
            return AgentAction(
                tool="write_file",
                arguments={
                    "path": "solution.py",
                    "content": "def fibonacci_fast(n):\n"
                               "    if n <= 1:\n"
                               "        return n\n"
                               "\n"
                               "    a, b = 0, 1\n"
                               "    for _ in range(2, n + 1):\n"
                               "        a, b = b, a + b\n"
                               "    return b"
                },
                description="Write the Fibonacci function to solution.py"
            )

        latest_test_entry = None
        for obs in reversed(state.observations):
            if "pytest" in obs:
                latest_test_entry = obs
                break

        if latest_test_entry:
            if 'success: False' in latest_test_entry:
                # If the tests have failed, run again
                return AgentAction(
                    tool="run_command",
                    arguments={
                        "command": "pytest test_solution.py"
                    },
                    description="Run pytest on the solution file"
                )
        else:
            # If the tests have not been run, run them
            return AgentAction(
                tool="run_command",
                arguments={
                    "command": "pytest test_solution.py"
                },
                description="Run pytest on the solution file"
            )
