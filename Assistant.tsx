import { useEffect, useMemo, useRef, useState } from "react";
import {
  Bot,
  Send,
  Sparkles,
  Shield,
  User,
  Trash2,
  AlertTriangle,
  RefreshCw,
} from "lucide-react";

type Finding = {
  id: string;
  title: string;
  severity: string;
  service: string;
  resource: string;
  description: string;
  evidence: string;
  risk: string;
  business_impact: string;
  recommendation: string;
  remediation: string;
  compliance: string[];
  status: string;
  risk_score: number;
  risk_level: string;
};

type ChatMessage = {
  id: number;
  role: "user" | "assistant";
  content: string;
};

const API_URL = "http://127.0.0.1:8000";

const QUICK_QUESTIONS = [
  "What are my critical findings?",
  "Explain my IAM risks",
  "What is SIEM?",
  "What is GRC?",
  "How do I fix open SSH?",
  "Summarize my CloudGuard scan",
];

function getGreetingResponse(message: string): string | null {
  const text = message.toLowerCase().trim();

  const greetings = [
    "hi",
    "hello",
    "hey",
    "hey there",
    "hi there",
    "yo",
    "good morning",
    "good afternoon",
    "good evening",
  ];

  if (greetings.includes(text)) {
    if (text.includes("morning")) {
      return "Good morning! 👋 I'm CloudGuard AI. What can I help you with today?";
    }

    if (text.includes("afternoon")) {
      return "Good afternoon! 👋 I'm CloudGuard AI. What can I help you with?";
    }

    if (text.includes("evening")) {
      return "Good evening! 👋 I'm CloudGuard AI. What can I help you with?";
    }

    return "Hey! 👋 I'm CloudGuard AI. I can help with CloudGuard, cloud security, cybersecurity, GRC, compliance, or general security questions. What would you like to know?";
  }

  if (
    text.includes("what's up") ||
    text.includes("whats up")
  ) {
    return "Hey! 😄 I'm doing great and ready to help. Ask me anything about CloudGuard or cybersecurity.";
  }

  if (
    text === "thanks" ||
    text === "thank you" ||
    text === "thx"
  ) {
    return "You're welcome! 😊 Let me know if you want to explore anything else.";
  }

  if (
    text === "bye" ||
    text === "goodbye"
  ) {
    return "Bye! 👋 Stay secure, and I'll be here whenever you need me.";
  }

  return null;
}

export default function Assistant() {
  const [findings, setFindings] = useState<Finding[]>([]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const [backendOnline, setBackendOnline] = useState(false);

  const [messages, setMessages] = useState<ChatMessage[]>([
    {
      id: 1,
      role: "assistant",
      content:
        "Hey! 👋 I'm CloudGuard AI. I'm your cybersecurity assistant for this project. Ask me about CloudGuard, your findings, cloud security, GRC, SOC, SIEM, IAM, compliance, or any cybersecurity topic.",
    },
  ]);

  const messagesEndRef = useRef<HTMLDivElement | null>(null);

  useEffect(() => {
    loadScannerData();
    checkBackend();
  }, []);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({
      behavior: "smooth",
    });
  }, [messages, loading]);

  async function checkBackend() {
    try {
      const response = await fetch(`${API_URL}/`, {
        method: "GET",
      });

      setBackendOnline(response.ok);
    } catch {
      setBackendOnline(false);
    }
  }

  async function loadScannerData() {
    try {
      const response = await fetch(
        `${API_URL}/api/scan/sample`
      );

      if (!response.ok) {
        throw new Error(
          `Scanner returned ${response.status}`
        );
      }

      const data = await response.json();

      setFindings(data.findings ?? []);
    } catch (error) {
      console.error(
        "Unable to load CloudGuard findings:",
        error
      );

      setFindings([]);
    }
  }

  const riskSummary = useMemo(() => {
    return {
      total: findings.length,

      critical: findings.filter(
        (finding) =>
          finding.severity === "Critical"
      ).length,

      high: findings.filter(
        (finding) =>
          finding.severity === "High"
      ).length,

      medium: findings.filter(
        (finding) =>
          finding.severity === "Medium"
      ).length,
    };
  }, [findings]);

  async function askCloudGuardAI(
    question: string
  ): Promise<string> {
    /*
     * Handle basic greetings immediately.
     * This means "hi" never depends on scanner findings.
     */
    const greeting = getGreetingResponse(
      question
    );

    if (greeting) {
      return greeting;
    }

    /*
     * Send the conversation to the FastAPI backend.
     */
    const history = messages.map((message) => ({
      role: message.role,
      content: message.content,
    }));

    const response = await fetch(
      `${API_URL}/api/assistant`,
      {
        method: "POST",

        headers: {
          "Content-Type": "application/json",
        },

        body: JSON.stringify({
          message: question,
          history,
        }),
      }
    );

    if (!response.ok) {
      let detail = "";

      try {
        const errorData = await response.json();

        detail =
          typeof errorData?.detail === "string"
            ? errorData.detail
            : "";
      } catch {
        // Ignore invalid error response.
      }

      throw new Error(
        detail ||
          `CloudGuard AI returned HTTP ${response.status}`
      );
    }

    const data = await response.json();

    return (
      data.answer ||
      "I received your question, but the AI service did not return an answer."
    );
  }

  async function sendMessage(
    text?: string
  ) {
    const question = (
      text ?? input
    ).trim();

    if (!question || loading) {
      return;
    }

    const userMessage: ChatMessage = {
      id: Date.now(),
      role: "user",
      content: question,
    };

    setMessages((current) => [
      ...current,
      userMessage,
    ]);

    setInput("");
    setLoading(true);

    try {
      const answer =
        await askCloudGuardAI(question);

      const assistantMessage: ChatMessage = {
        id: Date.now() + 1,
        role: "assistant",
        content: answer,
      };

      setMessages((current) => [
        ...current,
        assistantMessage,
      ]);
    } catch (error) {
      console.error(
        "CloudGuard AI error:",
        error
      );

      const errorMessage: ChatMessage = {
        id: Date.now() + 1,
        role: "assistant",
        content:
          "I couldn't reach the CloudGuard AI backend right now. Please make sure the FastAPI backend is running on http://127.0.0.1:8000 and try again.",
      };

      setMessages((current) => [
        ...current,
        errorMessage,
      ]);

      setBackendOnline(false);
    } finally {
      setLoading(false);
    }
  }

  function clearChat() {
    setMessages([
      {
        id: Date.now(),
        role: "assistant",
        content:
          "Chat cleared. 👋 I'm ready. Ask me anything about CloudGuard, cybersecurity, GRC, cloud security, or your security findings.",
      },
    ]);
  }

  return (
    <main className="min-h-[calc(100vh-80px)] bg-black p-6 text-white">
      <div className="mx-auto flex h-[calc(100vh-128px)] max-w-7xl flex-col gap-5">
        {/* ================================================= */}
        {/* HEADER */}
        {/* ================================================= */}

        <div className="flex flex-col justify-between gap-4 lg:flex-row lg:items-center">
          <div className="flex items-center gap-4">
            <div className="flex h-12 w-12 items-center justify-center rounded-xl border border-green-500/30 bg-green-500/5 shadow-[0_0_20px_rgba(34,197,94,0.08)]">
              <Bot className="h-6 w-6 text-green-400" />
            </div>

            <div>
              <div className="flex items-center gap-3">
                <h1 className="text-2xl font-bold">
                  AI Security Assistant
                </h1>

                <span className="rounded-full border border-green-500/30 bg-green-500/5 px-2.5 py-1 text-[10px] font-bold uppercase tracking-wider text-green-400">
                  CloudGuard AI
                </span>
              </div>

              <p className="mt-1 text-sm text-slate-500">
                Cybersecurity, cloud security,
                CloudGuard analysis and general
                security assistance.
              </p>
            </div>
          </div>

          <button
            onClick={clearChat}
            className="inline-flex items-center justify-center gap-2 rounded-xl border border-slate-800 bg-[#050505] px-4 py-2.5 text-sm text-slate-400 transition hover:border-red-500/40 hover:text-red-400"
          >
            <Trash2 size={15} />
            Clear Chat
          </button>
        </div>

        {/* ================================================= */}
        {/* STATUS */}
        {/* ================================================= */}

        <div className="flex flex-wrap items-center justify-between gap-3 rounded-xl border border-slate-900 bg-[#050505] px-4 py-3">
          <div className="flex items-center gap-3">
            <div
              className={`h-2.5 w-2.5 rounded-full ${
                backendOnline
                  ? "bg-green-400 shadow-[0_0_10px_rgba(34,197,94,0.9)]"
                  : "bg-red-500 shadow-[0_0_10px_rgba(239,68,68,0.8)]"
              }`}
            />

            <div>
              <p className="text-sm font-medium text-slate-300">
                {backendOnline
                  ? "CloudGuard AI backend connected"
                  : "AI backend unavailable"}
              </p>

              <p className="text-xs text-slate-600">
                {findings.length > 0
                  ? `${findings.length} CloudGuard findings available`
                  : "Project findings are not currently loaded"}
              </p>
            </div>
          </div>

          <div className="flex items-center gap-4 text-xs text-slate-600">
            <span>
              Critical{" "}
              <strong className="text-red-400">
                {riskSummary.critical}
              </strong>
            </span>

            <span>
              High{" "}
              <strong className="text-orange-400">
                {riskSummary.high}
              </strong>
            </span>

            <span>
              Total{" "}
              <strong className="text-white">
                {riskSummary.total}
              </strong>
            </span>

            <button
              onClick={() => {
                loadScannerData();
                checkBackend();
              }}
              className="rounded-lg p-2 transition hover:bg-red-500/10 hover:text-red-400"
              title="Refresh"
            >
              <RefreshCw size={14} />
            </button>
          </div>
        </div>

        {/* ================================================= */}
        {/* CHAT */}
        {/* ================================================= */}

        <div className="flex min-h-0 flex-1 flex-col overflow-hidden rounded-2xl border border-slate-900 bg-[#030303] shadow-[0_0_40px_rgba(0,0,0,0.4)]">
          {/* Chat header */}

          <div className="flex items-center justify-between border-b border-slate-900 bg-[#050505] px-5 py-4">
            <div className="flex items-center gap-3">
              <div className="flex h-9 w-9 items-center justify-center rounded-full border border-green-500/30 bg-green-500/5">
                <Sparkles className="h-4 w-4 text-green-400" />
              </div>

              <div>
                <p className="text-sm font-semibold text-white">
                  CloudGuard AI
                </p>

                <p className="text-xs text-slate-600">
                  Ask anything about cybersecurity
                </p>
              </div>
            </div>

            <div className="flex items-center gap-2 rounded-full border border-green-500/20 bg-green-500/5 px-3 py-1.5">
              <div className="h-1.5 w-1.5 rounded-full bg-green-400" />

              <span className="text-[10px] font-semibold uppercase tracking-wider text-green-400">
                Online
              </span>
            </div>
          </div>

          {/* Messages */}

          <div className="min-h-0 flex-1 overflow-y-auto p-5">
            <div className="mx-auto max-w-4xl space-y-5">
              {messages.map((message) => (
                <div
                  key={message.id}
                  className={`flex gap-3 ${
                    message.role === "user"
                      ? "justify-end"
                      : "justify-start"
                  }`}
                >
                  {message.role ===
                    "assistant" && (
                    <div className="flex h-9 w-9 shrink-0 items-center justify-center rounded-full border border-green-500/30 bg-green-500/5">
                      <Bot
                        size={16}
                        className="text-green-400"
                      />
                    </div>
                  )}

                  <div
                    className={`max-w-[82%] rounded-2xl px-4 py-3 ${
                      message.role ===
                      "user"
                        ? "rounded-br-md bg-red-600 text-white"
                        : "rounded-bl-md border border-slate-800 bg-[#080808] text-slate-200"
                    }`}
                  >
                    <p className="whitespace-pre-wrap text-sm leading-6">
                      {message.content}
                    </p>
                  </div>

                  {message.role === "user" && (
                    <div className="flex h-9 w-9 shrink-0 items-center justify-center rounded-full border border-red-500/30 bg-red-500/5">
                      <User
                        size={16}
                        className="text-red-400"
                      />
                    </div>
                  )}
                </div>
              ))}

              {loading && (
                <div className="flex gap-3">
                  <div className="flex h-9 w-9 shrink-0 items-center justify-center rounded-full border border-green-500/30 bg-green-500/5">
                    <Bot
                      size={16}
                      className="text-green-400"
                    />
                  </div>

                  <div className="rounded-2xl rounded-bl-md border border-slate-800 bg-[#080808] px-4 py-3">
                    <div className="flex items-center gap-2">
                      <div className="h-2 w-2 animate-pulse rounded-full bg-green-400" />
                      <div className="h-2 w-2 animate-pulse rounded-full bg-green-400 [animation-delay:150ms]" />
                      <div className="h-2 w-2 animate-pulse rounded-full bg-green-400 [animation-delay:300ms]" />

                      <span className="ml-2 text-xs text-slate-600">
                        CloudGuard AI is thinking...
                      </span>
                    </div>
                  </div>
                </div>
              )}

              <div ref={messagesEndRef} />
            </div>
          </div>

          {/* ================================================= */}
          {/* QUICK QUESTIONS */}
          {/* ================================================= */}

          <div className="border-t border-slate-900 bg-[#050505] px-5 py-3">
            <p className="mb-2 text-[10px] font-semibold uppercase tracking-wider text-slate-700">
              Try asking
            </p>

            <div className="flex gap-2 overflow-x-auto pb-1">
              {QUICK_QUESTIONS.map(
                (question) => (
                  <button
                    key={question}
                    onClick={() =>
                      sendMessage(question)
                    }
                    disabled={loading}
                    className="whitespace-nowrap rounded-lg border border-slate-800 bg-black px-3 py-2 text-xs text-slate-500 transition hover:border-green-500/30 hover:text-green-400 disabled:opacity-40"
                  >
                    {question}
                  </button>
                )
              )}
            </div>
          </div>

          {/* ================================================= */}
          {/* INPUT */}
          {/* ================================================= */}

          <div className="border-t border-slate-900 bg-black p-4">
            <div className="mx-auto flex max-w-4xl items-end gap-3">
              <textarea
                value={input}
                onChange={(event) =>
                  setInput(
                    event.target.value
                  )
                }
                onKeyDown={(event) => {
                  if (
                    event.key ===
                      "Enter" &&
                    !event.shiftKey
                  ) {
                    event.preventDefault();

                    sendMessage();
                  }
                }}
                placeholder="Ask anything about cybersecurity..."
                rows={2}
                disabled={loading}
                className="min-h-[52px] flex-1 resize-none rounded-xl border border-slate-800 bg-[#050505] px-4 py-3 text-sm text-white outline-none transition placeholder:text-slate-700 focus:border-red-500/50 disabled:opacity-50"
              />

              <button
                onClick={() =>
                  sendMessage()
                }
                disabled={
                  !input.trim() ||
                  loading
                }
                className="flex h-[52px] w-[52px] shrink-0 items-center justify-center rounded-xl bg-red-600 text-white shadow-[0_0_20px_rgba(239,68,68,0.08)] transition hover:bg-red-500 disabled:cursor-not-allowed disabled:opacity-30"
              >
                <Send size={18} />
              </button>
            </div>

            <p className="mt-2 text-center text-[10px] text-slate-700">
              CloudGuard AI can answer cybersecurity
              questions and analyze the current
              CloudGuard assessment.
            </p>
          </div>
        </div>
      </div>
    </main>
  );
}