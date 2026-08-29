
from harness.events import emit


def main():
    emit(
        "backend_started",
        message="AI Agent Harness backend started"
        )


if __name__ == "__main__":
    main()
