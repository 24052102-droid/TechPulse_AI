import React, { useState } from "react";
import { Tag } from "lucide-react";

export function DomainTag({ domain, confidence, isPrimary = false }) {
  const [showTooltip, setShowTooltip] = useState(false);
  const confPercent = Math.round((confidence || 0.8) * 100);

  const colors = {
    "Natural Language Processing": "text-blue-400 bg-blue-500/10 border-blue-500/20",
    "Computer Vision": "text-purple-400 bg-purple-500/10 border-purple-500/20",
    "Reinforcement Learning": "text-emerald-400 bg-emerald-500/10 border-emerald-500/20",
    "IoT and Embedded Systems": "text-teal-400 bg-teal-500/10 border-teal-500/20",
    "Systems and Infrastructure": "text-cyan-400 bg-cyan-500/10 border-cyan-500/20",
    "Robotics": "text-orange-400 bg-orange-500/10 border-orange-500/20",
    "Security and Privacy": "text-rose-400 bg-rose-500/10 border-rose-500/20",
    "Data Engineering and Pipelines": "text-indigo-400 bg-indigo-500/10 border-indigo-500/20",
    "Multimodal and Foundation Models": "text-fuchsia-400 bg-fuchsia-500/10 border-fuchsia-500/20",
    "General Machine Learning": "text-slate-300 bg-slate-500/10 border-slate-500/20",
  };

  const colorCls = colors[domain] || "text-slate-300 bg-slate-500/10 border-slate-500/20";

  return (
    <div
      className="relative inline-block"
      onMouseEnter={() => setShowTooltip(true)}
      onMouseLeave={() => setShowTooltip(false)}
    >
      <span
        className={`inline-flex items-center gap-1 px-2.5 py-0.5 rounded-md text-xs font-medium border cursor-help transition-all ${colorCls} ${
          isPrimary ? "font-semibold shadow-sm" : "opacity-80"
        }`}
      >
        <Tag className="w-2.5 h-2.5 opacity-70" />
        <span>{domain}</span>
        {isPrimary && (
          <span className="font-mono text-[10px] ml-0.5 opacity-80">· {confPercent}%</span>
        )}
      </span>

      {showTooltip && (
        <div className="absolute z-30 bottom-full left-0 mb-1.5 px-2.5 py-1.5 rounded-lg bg-obsidian-900 border border-slate-700/80 text-xs shadow-xl whitespace-nowrap text-slate-200">
          <p className="font-semibold text-emerald-400">Zero-Shot Domain Classifier</p>
          <p className="text-[11px] text-slate-300">
            Domain: <span className="text-white">{domain}</span>
          </p>
          <p className="text-[11px] text-slate-300">
            Confidence: <span className="font-mono text-emerald-300">{(confidence || 0.8).toFixed(2)} ({confPercent}%)</span>
          </p>
          <p className="text-[10px] text-slate-400 mt-0.5">Model: facebook/bart-large-mnli</p>
        </div>
      )}
    </div>
  );
}
