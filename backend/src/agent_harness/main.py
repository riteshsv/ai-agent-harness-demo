import json
import sys

def emit(event_type: str, **data):
    event = {
        "type": event_type, 
        **data
        }
    print(json.dumps(event),flush=True)




def main():
    emit(
        "backend_started",
        message="AI Agent Harness backend started"
        )


if __name__ == "__main__":
    main()
