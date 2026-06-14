"use client";

import { useState } from "react";
import TextareaAutosize from "react-textarea-autosize";
import { useWebSocket } from "./hooks/useWebSocket";

export default function Home() {
  const { messages, sendMessage, pendingApproval, respondToApproval } =
    useWebSocket();

  const [input, setInput] = useState("");

  const handleSend = () => {
    sendMessage(input);
    setInput("");
  };

  return (
    <div className="h-screen flex flex-col overflow-hidden">
      <div className="p-4 text-center text-olive-200 font-semibold shrink-0">
        ReWOO Assistant
      </div>

      <div className="flex-1 flex justify-center overflow-hidden">
        <div className="w-full max-w-3xl flex flex-col h-full">
          <div className="flex-1 overflow-y-auto px-4 py-2 space-y-4">
            {messages.map((msg, i) => {
              if (msg.role === "plan") {
                return (
                  <div key={i} className="flex justify-start">
                    <div className="bg-olive-800/40 border border-olive-600 rounded-lg p-3 max-w-6xl text-olive-200">
                      <div className="text-xs mb-2 opacity-70">Thinking...</div>

                      <ul className="list-disc pl-4 space-y-1 text-sm">
                        {msg.content.map((step, idx) => (
                          <li key={idx}>{step}</li>
                        ))}
                      </ul>
                    </div>
                  </div>
                );
              }

              return (
                <div
                  key={i}
                  className={`flex ${
                    msg.role === "user" ? "justify-end" : "justify-start"
                  }`}
                >
                  <div
                    className={`px-4 py-2 rounded-lg max-w-6xl text-sm whitespace-pre-wrap shadow ${
                      msg.role === "user"
                        ? "bg-olive-700 text-olive-100"
                        : "bg-olive-200 text-olive-900"
                    }`}
                  >
                    {msg.content}
                  </div>
                </div>
              );
            })}

            {pendingApproval && (
              <div className="flex justify-start">
                <div className="bg-yellow-100 text-yellow-950 border border-yellow-500 rounded-lg p-4 max-w-6xl text-sm shadow space-y-3">
                  <div className="font-semibold">Approval required</div>

                  <div>{pendingApproval.message}</div>

                  {pendingApproval.tool_name && (
                    <div>
                      Tool:{" "}
                      <span className="font-mono">
                        {pendingApproval.tool_name}
                      </span>
                    </div>
                  )}

                  {pendingApproval.tool_input && (
                    <pre className="text-xs bg-yellow-50 border border-yellow-300 rounded p-2 overflow-x-auto">
                      {JSON.stringify(pendingApproval.tool_input, null, 2)}
                    </pre>
                  )}

                  <div className="flex gap-2">
                    <button
                      onClick={() => respondToApproval(true)}
                      className="px-4 py-2 rounded bg-green-700 text-white hover:bg-green-600"
                    >
                      Approve
                    </button>

                    <button
                      onClick={() => respondToApproval(false)}
                      className="px-4 py-2 rounded bg-red-700 text-white hover:bg-red-600"
                    >
                      Reject
                    </button>
                  </div>
                </div>
              </div>
            )}
          </div>

          <div className="shrink-0 p-3">
            <div className="flex flex-col overflow-hidden gap-2 border rounded-xl border-olive-700/70 bg-olive-800/30">
              <TextareaAutosize
                value={input}
                onChange={(e) => setInput(e.target.value)}
                placeholder={
                  pendingApproval
                    ? "Approve or reject the pending action first..."
                    : "Ask anything..."
                }
                disabled={Boolean(pendingApproval)}
                className="px-4 py-2 rounded-lg outline-none resize-none text-olive-100 placeholder:text-olive-400 disabled:opacity-50"
                onKeyDown={(e) => {
                  if (e.key === "Enter" && !e.shiftKey) {
                    e.preventDefault();
                    handleSend();
                  }
                }}
                minRows={1}
                maxRows={6}
              />

              <div className="flex justify-end px-2 pb-2">
                <button
                  onClick={handleSend}
                  disabled={Boolean(pendingApproval)}
                  className="px-5 py-2 rounded-lg bg-olive-700 hover:bg-olive-600 disabled:opacity-50 disabled:cursor-not-allowed transition-all text-olive-100"
                >
                  Send
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
