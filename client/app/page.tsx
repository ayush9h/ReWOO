"use client";

import { useState } from "react";
import { useWebSocket } from "./hooks/useWebSocket";
import TextareaAutosize from "react-textarea-autosize";


export default function Home() {
  const { messages, sendMessage } = useWebSocket();
  const [input, setInput] = useState("");

  return (
    <div className="h-screen flex flex-col  overflow-hidden">
      <div className="p-4 text-center text-olive-200 font-semibold shrink-0">
        ReWOO and Human in the Loop Integrated Assistant
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
          </div>

          <div className="shrink-0 p-3">
            <div className="flex flex-col  overflow-hidden gap-2 border rounded-xl border-olive-700/70 bg-olive-800/30">
              <TextareaAutosize
                value={input}
                onChange={(e) => setInput(e.target.value)}
                placeholder="Ask anything..."
                className="px-4 py-2 rounded-lg outline-none resize-none  text-olive-100 placeholder:text-olive-400"
                onKeyDown={(e) => {
                  if (e.key === "Enter" && !e.shiftKey) {
                    e.preventDefault();
                    sendMessage(input);
                    setInput("")
                  }
                }}
                minRows={1}
                maxRows={6}
              />

              <div className="flex justify-end px-2 pb-2">
                <button
                  onClick={() => {
                    sendMessage(input);
                    setInput("");
                  }}
                  className="px-5 py-2 rounded-lg bg-olive-700 hover:bg-olive-600 transition-all text-olive-100"
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
