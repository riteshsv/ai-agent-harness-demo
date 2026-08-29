import React, { useEffect, useState } from "react";
import { Box, Text } from "ink";
import { startBackend, BackendEvent } from "../backend/backendProcess.js";

export function App() {
  const [backendConnected, setBackendConnected] = useState(false);
  const [lastEvent, setLastEvent] = useState<BackendEvent | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const backend = startBackend(
      (event) => {
        setLastEvent(event);

        if (event.type === "backend_started") {
          setBackendConnected(true);
        }
      },
      (err) => {
        setError(err.message);
      },
    );

    return () => {
      backend.kill();
    };
  }, []);

  return (
    <Box flexDirection="column" padding={1}>
      <Text bold>
        ╔══════════════════════════════════════╗
      </Text>

      <Text bold>
        ║       AI AGENT HARNESS DEMO          ║
      </Text>

      <Text bold>
        ╚══════════════════════════════════════╝
      </Text>

      <Box marginTop={1} flexDirection="column">
        <Text>
          Backend:{" "}
          <Text color={backendConnected ? "green" : "yellow"}>
            {backendConnected ? "CONNECTED" : "CONNECTING..."}
          </Text>
        </Text>

        <Text>
          Harness: <Text color="yellow">INITIALIZING</Text>
        </Text>

        <Text>
          RALPH: <Text color="gray">NOT STARTED</Text>
        </Text>
      </Box>

      <Box marginTop={1} flexDirection="column">
        <Text bold>Last Event</Text>

        <Text>
          {lastEvent
            ? JSON.stringify(lastEvent)
            : "Waiting for backend..."}
        </Text>
      </Box>

      {error && (
        <Box marginTop={1}>
          <Text color="red">Error: {error}</Text>
        </Box>
      )}
    </Box>
  );
}