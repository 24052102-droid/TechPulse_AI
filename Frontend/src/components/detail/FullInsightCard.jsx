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

      {/* Limitations & Research Gaps (Opportunity Detector) */}
      <div className="glass-panel p-6 rounded-2xl border-amber-500/20 bg-gradient-to-b from-obsidian-850 to-obsidian-900">
        <div className="flex items-center gap-2 text-amber-400 font-bold text-xs uppercase tracking-wider mb-3">
          <AlertCircle className="w-4 h-4" />
          <span>Limitations & Candidate Research Gaps</span>
        </div>
        <div className="space-y-2 text-xs text-slate-300 leading-relaxed">
          <p>
            • Primary empirical evaluation is constrained to standard benchmarking distributions;
            behavior under adversarial noise or extreme thermal constraints remains an open investigation.
          </p>
          <p>
            • <strong>Opportunity:</strong> Candidate direction for follow-up work involves testing dynamic
            quantization with low-precision floating point representations on edge hardware.
          </p>
        </div>
      </div>

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
