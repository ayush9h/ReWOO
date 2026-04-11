"use client";
import { useEffect, useState } from "react";

interface Message {
  role: "user" | "assistant";
  content: string;
}

const API_BASE = "127.0.0.1:8000/v1/conversation";

export function useWebSocket() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [ws, setWs] = useState<WebSocket | null>(null);

  useEffect(() => {
    const init = async () => {
      try {
        const res = await fetch(`http://${API_BASE}/c`, {
          method: "POST",
        });

        if (!res.ok)
          throw new Error(`HTTP error occurred due to: ${res.statusText}`);
        const { request_id } = await res.json();

        // Establishes the socket connection
        const ws = new WebSocket(`ws://${API_BASE}/c/${request_id}`);

        ws.onopen = () => {
          console.log("Connected successfully through the websocket server");
        };

        setWs(ws);

        // Stream the events on the UI
        ws.onmessage = (event) => {
          const payload = JSON.parse(event.data);

          if (payload.type === "plan" || payload.type === "summarizer") {
            setMessages((prev) => [
              ...prev,
              {
                role: "assistant",
                content: payload.data,
              },
            ]);
          }
        };
        return () => {
          ws?.close();
        };
      } catch (err) {
        console.log(err);
      }
    };

    init();
  }, []);

  //   Send the user the message
  const sendMessage = (input: string) => {
    if (!ws || ws.readyState !== WebSocket.OPEN) {
      setMessages((prev) => [
        ...prev,
        { role: "assistant", content: "Socket not connected" },
      ]);
      return;
    }

    if (!input.trim()) return;

    // Quries the backend
    ws.send(JSON.stringify({ query: input }));

    setMessages((prev) => [...prev, { role: "user", content: input }]);
  };

  return { messages, sendMessage };
}
