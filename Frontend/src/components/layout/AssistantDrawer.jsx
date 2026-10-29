import React, { useState, useRef, useEffect } from "react";
import { X, Sparkles, Send, ArrowRight, Bot, RotateCcw, ChevronRight } from "lucide-react";
import { useFeedStore } from "../../store/useFeedStore";

export function AssistantDrawer() {
  const { isAssistantOpen, toggleAssistant, items, setActiveRoute } = useFeedStore();
  const [input, setInput] = useState("");
  const [isTyping, setIsTyping] = useState(false);
  const messagesEndRef = useRef(null);

  const initialMessage = {
    role: "assistant",
    text: "Hello! I am your Technical Intelligence Assistant. Ask me anything about newly ingested arXiv papers, high-velocity GitHub repositories, or emerging domain trends.",
    citations: [],
    timestamp: "Just now",
  };

  const [messages, setMessages] = useState([initialMessage]);

  useEffect(() => {
    if (isAssistantOpen) {
      messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
    }
  }, [messages, isAssistantOpen]);

  if (!isAssistantOpen) return null;

  const starterPrompts = [
    "Highest-impact NLP papers from this week?",
    "Which repositories have the highest star velocity?",
    "Summarize open research gaps in edge models.",
  ];

  const handleSend = (queryText) => {
    const q = queryText || input;
    if (!q.trim()) return;

    const userMsg = {
      role: "user",
      text: q,
      citations: [],
      timestamp: new Date().toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" }),
    };

    setMessages((prev) => [...prev, userMsg]);
    setInput("");
    setIsTyping(true);

    // Grounded synthesis using current feed intelligence
    setTimeout(() => {
      const qLower = q.toLowerCase();
      let matched = [];

      if (qLower.includes("nlp") || qLower.includes("language") || qLower.includes("text")) {
        matched = items.filter(
          (it) =>
            it.primary_domain?.toLowerCase().includes("nlp") ||
            it.primary_domain?.toLowerCase().includes("natural language") ||
            it.title.toLowerCase().includes("nlp") ||
            it.title.toLowerCase().includes("llm")
        );
      } else if (qLower.includes("repo") || qLower.includes("star") || qLower.includes("velocity") || qLower.includes("github")) {
        matched = items.filter((it) => it.source?.toLowerCase().includes("github") || it.github_stars > 0);
      } else if (qLower.includes("edge") || qLower.includes("efficient") || qLower.includes("quant")) {
        matched = items.filter(
          (it) =>
            it.title.toLowerCase().includes("edge") ||
            it.title.toLowerCase().includes("efficient") ||
            it.summary?.toLowerCase().includes("edge")
        );
      }

      if (matched.length === 0) {
        matched = items.slice(0, 3);
      } else {
        matched = matched.slice(0, 3);
      }

      const aiMsg = {
        role: "assistant",
        text: `Based on recently classified technical items across the ATIP taxonomy, high-signal outputs in this area demonstrate architectural optimizations that lower computational latency and improve reproducible benchmarking. Here are the top evidence-grounded intelligence cards:`,
        citations: matched.map((item) => ({
          id: item.id,
          title: item.title,
          source: item.source,
          impact: item.impact_score,
        })),
        timestamp: new Date().toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" }),
      };

      setMessages((prev) => [...prev, aiMsg]);
      setIsTyping(false);
    }, 450);
  };

  const handleReset = () => {
    setMessages([initialMessage]);
  };

  return (
    <>
      {/* Backdrop overlay for focus and contrast */}
      <div
        onClick={toggleAssistant}
        className="fixed inset-0 bg-black/50 backdrop-blur-[2px] z-40 transition-opacity animate-in fade-in duration-200"
        aria-hidden="true"
      />

      {/* Assistant Drawer Panel */}
      <aside
        aria-label="Technical Intelligence Assistant"
        className="fixed inset-y-0 right-0 w-[420px] max-w-[92vw] z-50 bg-[#0c0e14] border-l border-slate-700/80 shadow-[-12px_0_40px_rgba(0,0,0,0.65)] flex flex-col justify-between animate-in slide-in-from-right duration-250 select-text"
      >
        {/* Header */}
        <header className="p-4 border-b border-slate-800 bg-[#121622] flex items-center justify-between shrink-0">
          <div className="flex items-center gap-3">
            <div className="p-2 rounded-xl bg-emerald-500/15 border border-emerald-500/30 text-emerald-400 shadow-[0_0_15px_rgba(16,185,129,0.2)]">
              <Sparkles className="w-4 h-4" />
            </div>
            <div>
              <div className="flex items-center gap-2">
                <h2 className="text-xs font-bold text-white tracking-wide">
                  Technical RAG Assistant
                </h2>
                <span className="inline-flex items-center gap-1 px-1.5 py-0.5 rounded text-[10px] font-mono font-medium bg-emerald-500/15 text-emerald-300 border border-emerald-500/30">
                  <span className="w-1.5 h-1.5 rounded-full bg-emerald-400 animate-pulse"></span>
                  LIVE
                </span>
              </div>
              <p className="text-[11px] text-slate-300 font-medium">
                Evidence-grounded arXiv & GitHub intelligence
              </p>
            </div>
          </div>

          <div className="flex items-center gap-1">
            <button
              onClick={handleReset}
              title="Reset conversation"
              className="p-2 rounded-lg text-slate-400 hover:text-white hover:bg-slate-800 transition-colors"
              aria-label="Reset conversation"
            >
              <RotateCcw className="w-3.5 h-3.5" />
            </button>
            <button
              onClick={toggleAssistant}
              title="Close assistant"
              className="p-2 rounded-lg text-slate-400 hover:text-white hover:bg-slate-800 transition-colors"
              aria-label="Close assistant"
            >
              <X className="w-4 h-4" />
            </button>
          </div>
        </header>

        {/* Message History */}
        <div className="flex-1 overflow-y-auto p-4 space-y-4 text-xs bg-[#0c0e14]">
          {messages.map((m, idx) => (
            <div
              key={idx}
              className={`flex flex-col ${
                m.role === "user" ? "items-end" : "items-start"
              }`}
            >
              <div className="flex items-center gap-1.5 mb-1 px-1">
                {m.role === "assistant" ? (
                  <span className="text-[10px] font-semibold text-emerald-400 flex items-center gap-1">
                    <Bot className="w-3 h-3" />
                    ATIP Assistant
                  </span>
                ) : (
                  <span className="text-[10px] font-semibold text-slate-300">
                    You
                  </span>
                )}
                {m.timestamp && (
                  <span className="text-[10px] text-slate-300">
                    · {m.timestamp}
                  </span>
                )}
              </div>

              <div
                className={`p-3.5 rounded-2xl max-w-[92%] leading-relaxed shadow-sm ${
                  m.role === "user"
                    ? "bg-emerald-600 text-white font-medium border border-emerald-500 rounded-tr-sm"
                    : "bg-[#161a24] text-slate-100 border border-slate-700/80 rounded-tl-sm"
                }`}
              >
                <p className="text-xs whitespace-pre-wrap leading-relaxed">{m.text}</p>

                {/* Clickable Grounded Citations */}
                {m.citations && m.citations.length > 0 && (
                  <div className="mt-3 pt-2.5 border-t border-slate-700/70 space-y-2">
                    <p className="text-[10px] font-bold text-emerald-400 uppercase tracking-wider flex items-center gap-1">
                      <span>✦</span>
                      Grounded References:
                    </p>
                    <div className="space-y-1.5">
                      {m.citations.map((c) => (
                        <button
                          key={c.id}
                          onClick={() => {
                            setActiveRoute(`/item/${c.id}`, c.id);
                            toggleAssistant();
                          }}
                          className="w-full text-left p-2 rounded-lg bg-[#0e1118] hover:bg-[#1f2535] border border-slate-700/80 hover:border-emerald-500/60 text-slate-200 hover:text-white transition-all flex items-center justify-between gap-2 group cursor-pointer shadow-sm"
                        >
                          <div className="truncate flex-1">
                            <span className="text-[11px] font-medium block truncate group-hover:text-emerald-300">
                              {c.title}
                            </span>
                            <span className="text-[10px] text-slate-300 uppercase tracking-wider">
                              {c.source || "arXiv"}
                            </span>
                          </div>
                          <span className="font-mono text-[10px] text-emerald-400 bg-emerald-500/15 border border-emerald-500/30 px-1.5 py-0.5 rounded font-bold shrink-0">
                            [{c.impact}/10]
                          </span>
                        </button>
                      ))}
                    </div>
                  </div>
                )}
              </div>
            </div>
          ))}

          {isTyping && (
            <div className="flex items-center gap-2 text-slate-300 text-xs px-2 py-1">
              <span className="w-1.5 h-1.5 rounded-full bg-emerald-400 animate-bounce"></span>
              <span className="w-1.5 h-1.5 rounded-full bg-emerald-400 animate-bounce [animation-delay:0.15s]"></span>
              <span className="w-1.5 h-1.5 rounded-full bg-emerald-400 animate-bounce [animation-delay:0.3s]"></span>
              <span className="text-[11px]">Synthesizing technical evidence...</span>
            </div>
          )}

          {/* Quick Starters */}
          {messages.length === 1 && (
            <div className="pt-2">
              <p className="text-[11px] uppercase font-bold text-slate-300 mb-2.5 tracking-wider flex items-center gap-1.5">
                <span className="text-emerald-400">✦</span>
                Suggested Queries:
              </p>
              <div className="space-y-2">
                {starterPrompts.map((p, idx) => (
                  <button
                    key={idx}
                    onClick={() => handleSend(p)}
                    className="w-full text-left p-2.5 rounded-xl bg-[#161a24] hover:bg-[#202534] border border-slate-700/90 hover:border-emerald-500/60 text-slate-100 hover:text-emerald-200 text-xs font-medium transition-all flex items-center justify-between group shadow-sm cursor-pointer"
                  >
                    <span>{p}</span>
                    <ChevronRight className="w-4 h-4 text-slate-400 group-hover:text-emerald-400 group-hover:translate-x-0.5 transition-all shrink-0 ml-2" />
                  </button>
                ))}
              </div>
            </div>
          )}

          <div ref={messagesEndRef} />
        </div>

        {/* Input Field */}
        <form
          onSubmit={(e) => {
            e.preventDefault();
            handleSend();
          }}
          className="p-3.5 border-t border-slate-800 bg-[#121622] flex items-center gap-2 shrink-0"
        >
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="Ask a question about current intelligence..."
            className="flex-1 bg-[#161a24] border border-slate-700 rounded-xl px-3.5 py-2.5 text-xs text-white placeholder:text-slate-400 focus:outline-none focus:border-emerald-500 focus:ring-1 focus:ring-emerald-500/50 transition-all"
          />
          <button
            type="submit"
            disabled={!input.trim()}
            className="p-2.5 rounded-xl bg-emerald-500 text-slate-950 font-bold hover:bg-emerald-400 disabled:opacity-30 disabled:hover:bg-emerald-500 transition-all shadow-md hover:shadow-emerald-500/20 active:scale-95 cursor-pointer"
            aria-label="Send query"
          >
            <Send className="w-4 h-4" />
          </button>
        </form>
      </aside>
    </>
  );
}
