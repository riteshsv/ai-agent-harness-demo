import { spawn, ChildProcessWithoutNullStreams } from "node:child_process";
import readline from "node:readline";

export interface BackendEvent {
  type: string;
  [key: string]: unknown;
}

export function startBackend(
  onEvent: (event: BackendEvent) => void,
  onError: (error: Error) => void,
): ChildProcessWithoutNullStreams {
  const backend = spawn(
    "uv",
    ["run", "python", "-m", "src.agent_harness.main"],
    {
      cwd: "../backend",
      stdio: ["pipe", "pipe", "pipe"],
    },
  );

  const output = readline.createInterface({
    input: backend.stdout,
  });

  output.on("line", (line) => {
    if (!line.trim()) {
      return;
    }

    try {
      const event = JSON.parse(line) as BackendEvent;
      onEvent(event);
    } catch {
      onError(
        new Error(`Invalid JSON event received: ${line}`),
      );
    }
  });

  backend.stderr.on("data", (data: Buffer) => {
    const message = data.toString().trim();

    if (message) {
      onError(new Error(message));
    }
  });

  backend.on("error", onError);

  return backend;
}