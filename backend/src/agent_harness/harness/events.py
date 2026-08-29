import json
import sys

def emit(event_type: str, **data):
    """
    Emit an event to stdout in JSONL format.
    Any component of the harness can emit events
    Eg:
        emit(
        "iteration_started",
        iteration=1,
        )
    Output:
    {"type": "iteration_started", "iteration": 1}
    """
    event = {
        "type": event_type, 
        **data
        }
    print(json.dumps(event),flush=True)
