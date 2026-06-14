"use client";

import { useEffect, useRef, useState } from "react";
import TextareaAutosize from "react-textarea-autosize";
import { Check, Send, UserCheck2, X } from "lucide-react";

import { useWebSocket } from "./hooks/useWebSocket";

export default function Home() {
  const { messages, sendMessage, pendingApproval, respondToApproval } =
    useWebSocket();

  const [input, setInput] = useState("");
  const bottomRef = useRef<HTMLDivElement | null>(null);

  const hasPendingApproval = Boolean(pendingApproval);
  const canSend = input.trim().length > 0 && !hasPendingApproval;

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, pendingApproval]);

  const handleSend = () => {
    const value = input.trim();
    if (!value || hasPendingApproval) return;

    sendMessage(value);
    setInput("");
  };

  return (
    <main className="h-screen bg-slate-50 text-slate-950 flex flex-col overflow-hidden font-geist">
      <header className="h-14 shrink-0 border-b border-slate-200 bg-white">
        <div className="mx-auto h-full max-w-4xl px-4 flex items-center justify-center">
          <h1 className="text-base font-medium tracking-tight">
            ReWOO based Assistant
          </h1>
        </div>
      </header>

      <section className="flex-1 min-h-0 flex flex-col overflow-hidden">
        <div className="flex-1 min-h-0 overflow-y-auto">
          <div className="mx-auto max-w-4xl px-4 py-6">
            {messages.length === 0 && !pendingApproval && (
              <div className="min-h-[calc(100vh-220px)] flex items-center justify-center">
                <div className="text-center max-w-sm">
                  <h2 className="text-lg font-semibold">Ready when you are</h2>

                  <p className="mt-2 text-sm text-slate-500">
                    Start by asking a question
                  </p>
                </div>
              </div>
            )}

            <div className="space-y-5">
              {messages.map((msg, i) => {
                if (msg.role === "plan") {
                  const steps = Array.isArray(msg.content)
                    ? msg.content
                    : [String(msg.content)];

                  return (
                    <div key={i} className="flex justify-start">
                      <div className="w-full max-w-2xl rounded-lg border border-blue-100 bg-blue-50 p-4">
                        <div className="mb-3 flex items-center gap-2 text-blue-700">
                          <span className="text-xs font-medium uppercase tracking-wide">
                            Tasks to be executed
                          </span>
                        </div>

                        <ul className="space-y-2 text-sm text-slate-700">
                          {steps.map((step, idx) => (
                            <li key={idx} className="flex gap-2">
                              <span className="mt-2 size-1 rounded-full bg-blue-600 shrink-0" />
                              <span>{step}</span>
                            </li>
                          ))}
                        </ul>
                      </div>
                    </div>
                  );
                }

                const isUser = msg.role === "user";

                return (
                  <div
                    key={i}
                    className={`flex gap-3 ${
                      isUser ? "justify-end" : "justify-start"
                    }`}
                  >
                    <div
                      className={`max-w-2xl rounded-lg px-2 py-1.5 text-sm leading-6 whitespace-pre-wrap ${
                        isUser ? "bg-blue-600 text-white" : " text-slate-900"
                      }`}
                    >
                      {msg.content}
                    </div>
                  </div>
                );
              })}

              {pendingApproval && (
                <div className="flex justify-start">
                  <div className="w-full max-w-2xl rounded-lg border border-blue-100 bg-blue-50 p-4">
                    <div className="flex items-start gap-2">
                      <div className="size-8 rounded-lg bg-blue-600 text-white flex items-center justify-center">
                        <UserCheck2 size={17} />
                      </div>

                      <div className="min-w-0 flex-1">
                        <h3 className="text-sm font-semibold">
                          Approval required
                        </h3>

                        {pendingApproval.tool_name && (
                          <div className="mt-3 text-sm"></div>
                        )}

                        {pendingApproval.tool_input && (
                          <pre className="mt-3 max-h-64 overflow-auto rounded-lg border border-blue-100 bg-white p-3 text-xs leading-5 text-slate-800">
                            {JSON.stringify(
                              pendingApproval.tool_input,
                              null,
                              2,
                            )}
                          </pre>
                        )}

                        <div className="mt-4 flex gap-2">
                          <button
                            type="button"
                            onClick={() => respondToApproval(true)}
                            className="inline-flex items-center gap-2 rounded-lg bg-blue-600 px-3 py-2 text-sm font-medium text-white hover:bg-blue-700 transition"
                          >
                            <Check size={15} />
                            Approve
                          </button>

                          <button
                            type="button"
                            onClick={() => respondToApproval(false)}
                            className="inline-flex items-center gap-2 rounded-lg border border-slate-300 bg-white px-3 py-2 text-sm font-medium text-slate-800 hover:bg-slate-100 transition"
                          >
                            <X size={15} />
                            Reject
                          </button>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              )}

              <div ref={bottomRef} />
            </div>
          </div>
        </div>

        <footer className="pb-4">
          <div className="mx-auto max-w-4xl">
            <div className="rounded-lg border border-slate-300 bg-white focus-within:border-blue-500 focus-within:ring-2 focus-within:ring-blue-500/10 transition">
              <TextareaAutosize
                value={input}
                onChange={(e) => setInput(e.target.value)}
                placeholder={
                  hasPendingApproval
                    ? "Approve or reject the pending action first..."
                    : "Ask anything..."
                }
                disabled={hasPendingApproval}
                minRows={1}
                maxRows={6}
                className="w-full resize-none bg-transparent px-4 py-3 text-sm leading-6 text-slate-950 placeholder:text-slate-400 outline-none disabled:cursor-not-allowed disabled:opacity-50"
                onKeyDown={(e) => {
                  if (e.key === "Enter" && !e.shiftKey) {
                    e.preventDefault();
                    handleSend();
                  }
                }}
              />

              <div className="flex items-center justify-end px-3 pb-3">
                <button
                  type="button"
                  onClick={handleSend}
                  disabled={!canSend}
                  className="inline-flex items-center justify-center rounded-lg bg-blue-600 p-2 text-white hover:bg-blue-700 disabled:cursor-not-allowed disabled:opacity-50 transition"
                >
                  <Send size={16} />
                </button>
              </div>
            </div>
          </div>
        </footer>
      </section>
    </main>
  );
}
