"use client";

import { useEffect, useRef, useState } from "react";

type Message =
  | { role: "user"; content: string }
  | { role: "assistant"; content: string }
  | { role: "plan"; content: string[] };

type InterruptPayload = {
  message: string;
  tool_name?: string;
  tool_input?: Record<string, unknown>;
};

const API_BASE = "127.0.0.1:8000/v1/conversation";

export function useWebSocket() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [pendingApproval, setPendingApproval] =
    useState<InterruptPayload | null>(null);

  const wsRef = useRef<WebSocket | null>(null);

  useEffect(() => {
    let socket: WebSocket | null = null;

    const init = async () => {
      try {
        const res = await fetch(`http://${API_BASE}/c`, {
          method: "POST",
        });

        if (!res.ok) {
          throw new Error(`HTTP error occurred due to: ${res.statusText}`);
        }

        const { request_id } = await res.json();

        socket = new WebSocket(`ws://${API_BASE}/c/${request_id}`);
        wsRef.current = socket;

        socket.onopen = () => {
          console.log("Connected successfully through the websocket server");
        };

        socket.onmessage = (event) => {
          const payload = JSON.parse(event.data);

          if (payload.type === "plan") {
            setMessages((prev) => [
              ...prev,
              {
                role: "plan",
                content: payload.data,
              },
            ]);
          }

          if (payload.type === "summarizer") {
            setMessages((prev) => [
              ...prev,
              {
                role: "assistant",
                content: payload.data,
              },
            ]);
          }

          if (payload.type === "interrupt") {
            setPendingApproval(payload.data);

            setMessages((prev) => [
              ...prev,
              {
                role: "assistant",
                content:
                  payload.data?.message ??
                  "Approval required before continuing.",
              },
            ]);
          }

          if (payload.type === "error") {
            setMessages((prev) => [
              ...prev,
              {
                role: "assistant",
                content: payload.data,
              },
            ]);
          }
        };

        socket.onclose = () => {
          wsRef.current = null;
        };
      } catch (err) {
        console.error(err);
      }
    };

    init();

    return () => {
      socket?.close();
    };
  }, []);

  const sendMessage = (input: string) => {
    const ws = wsRef.current;

    if (!ws || ws.readyState !== WebSocket.OPEN) {
      setMessages((prev) => [
        ...prev,
        { role: "assistant", content: "Socket not connected" },
      ]);
      return;
    }

    if (!input.trim()) return;

    if (pendingApproval) {
      setMessages((prev) => [
        ...prev,
        {
          role: "assistant",
          content: "Please approve or reject the pending action first.",
        },
      ]);
      return;
    }

    ws.send(
      JSON.stringify({
        type: "query",
        query: input,
      }),
    );

    setMessages((prev) => [...prev, { role: "user", content: input }]);
  };

  const respondToApproval = (approved: boolean) => {
    const ws = wsRef.current;

    if (!ws || ws.readyState !== WebSocket.OPEN) {
      setMessages((prev) => [
        ...prev,
        { role: "assistant", content: "Socket not connected" },
      ]);
      return;
    }

    ws.send(
      JSON.stringify({
        type: "resume",
        approved,
      }),
    );

    setMessages((prev) => [
      ...prev,
      {
        role: "user",
        content: approved ? "Approved" : "Rejected",
      },
    ]);

    setPendingApproval(null);
  };

  return {
    messages,
    sendMessage,
    pendingApproval,
    respondToApproval,
  };
}
