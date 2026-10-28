import React, { useState } from "react";
import { Sparkles, CheckCircle2, AlertCircle, ChevronDown, ChevronUp, FileText } from "lucide-react";

export function FullInsightCard({ item, insight }) {
  const [showRaw, setShowRaw] = useState(false);

  return (
    <div className="space-y-6">
      {/* Executive Summary */}
      <div className="glass-panel p-6 rounded-2xl">
        <div className="flex items-center gap-2 text-emerald-400 font-bold text-xs uppercase tracking-wider mb-3">
          <Sparkles className="w-4 h-4" />
          <span>Executive Summary & Core Claim</span>
        </div>
        <p className="text-sm text-slate-200 leading-relaxed font-medium">
          {insight?.summary || item.description || "Summary not available."}
        </p>
      </div>

      {/* Key Takeaways */}
      {insight?.key_takeaways && (
        <div className="glass-panel p-6 rounded-2xl">
          <h4 className="text-xs font-bold text-slate-400 uppercase tracking-wider mb-4">
            Key Technical Takeaways
          </h4>
          <ul className="space-y-3">
            {insight.key_takeaways.map((point, idx) => (
              <li key={idx} className="flex items-start gap-3 text-xs text-slate-300 leading-relaxed">
                <CheckCircle2 className="w-4 h-4 text-emerald-400 shrink-0 mt-0.5" />
                <span>{point}</span>
              </li>
            ))}
          </ul>
        </div>
      )}

      {/* Why It Matters */}
      {insight?.why_it_matters && (
        <div className="glass-panel p-6 rounded-2xl">
          <h4 className="text-xs font-bold text-slate-400 uppercase tracking-wider mb-2">
            Why It Matters & Engineering Impact
          </h4>
          <p className="text-xs text-slate-300 leading-relaxed italic bg-obsidian-900/60 p-4 rounded-xl border border-slate-800">
            "{insight.why_it_matters}"
          </p>
        </div>
      )}

      {/* Technical Profile & Synthesis Metadata */}
      {insight && (
        <div className="glass-panel p-6 rounded-2xl border-outline-variant/40">
          <div className="flex items-center justify-between flex-wrap gap-2 mb-3">
            <span className="text-xs font-bold text-slate-400 uppercase tracking-wider">
              Technical Profile &amp; Taxonomy
            </span>
            <span className="font-code-sm text-code-sm text-secondary">
              {insight.llm_model ? `Synthesized by ${insight.llm_model}` : "AI Synthesis"}
            </span>
          </div>
          <div className="flex items-center gap-2 flex-wrap mb-3">
            <span className="px-2.5 py-1 rounded bg-[#EEF2FF] text-[#3730A3] font-code-sm text-code-sm font-semibold capitalize">
              {insight.technical_depth || "Intermediate"} Depth
            </span>
            <span className="px-2.5 py-1 rounded bg-surface-container text-secondary font-code-sm text-code-sm">
              Est. Read: {insight.estimated_read_time || 5} min
            </span>
          </div>
          {insight.related_topics && insight.related_topics.length > 0 && (
            <div className="flex items-center gap-1.5 flex-wrap">
              {insight.related_topics.map((topic, idx) => (
                <span
                  key={idx}
                  className="font-code-sm text-code-sm text-secondary bg-surface-container px-2 py-0.5 rounded"
                >
                  #{topic.replace("#", "")}
                </span>
              ))}
            </div>
          )}
        </div>
      )}

      {/* Collapsible Raw Source Text */}
      <div className="glass-panel p-6 rounded-2xl">
        <button
          onClick={() => setShowRaw(!showRaw)}
          className="w-full flex items-center justify-between text-xs font-semibold text-slate-300 hover:text-white"
        >
          <div className="flex items-center gap-2">
            <FileText className="w-4 h-4 text-slate-400" />
            <span>Raw {item.source === "arxiv" ? "Abstract" : "README"} Text</span>
          </div>
          {showRaw ? <ChevronUp className="w-4 h-4" /> : <ChevronDown className="w-4 h-4" />}
        </button>

        {showRaw && (
          <div className="mt-4 pt-4 border-t border-slate-800 text-xs text-slate-400 font-mono leading-relaxed bg-obsidian-950 p-4 rounded-xl max-h-60 overflow-y-auto">
            {item.description}
          </div>
        )}
      </div>
    </div>
  );
}
