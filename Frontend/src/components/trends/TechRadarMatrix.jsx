import React from "react";
import { Sparkles, Rocket, Landmark, TrendingDown, AlertTriangle } from "lucide-react";

export function TechRadarMatrix({ domains = [] }) {
  // Classify domains into quadrants based on wow_delta and hype_adoption_ratio
  const emerging = [];
  const rising = [];
  const established = [];
  const declining = [];

  domains.forEach((d) => {
    const wow = d.wow_delta || 0;
    const ratio = d.hype_adoption_ratio || 1.0;

    if (wow < -0.05) {
      declining.push(d);
    } else if (ratio > 1.8) {
      emerging.push({ ...d, tag: "High Research Hype" });
    } else if (d.is_trending || wow > 0.1) {
      rising.push({ ...d, tag: "Rapid Adoption" });
    } else {
      established.push({ ...d, tag: "Mature Production" });
    }
  });

  return (
    <div className="glass-panel p-6 rounded-2xl mb-8">
      <div className="flex items-center justify-between mb-6">
        <div>
          <h3 className="text-base font-bold text-white flex items-center gap-2">
            <Sparkles className="w-4 h-4 text-emerald-400" />
            <span>Technology Radar & Hype vs. Adoption Matrix</span>
          </h3>
          <p className="text-xs text-slate-400">
            Categorizing technical domains by academic velocity vs. open-source software adoption
          </p>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        {/* Quadrant 1: Emerging */}
        <div className="p-4 rounded-xl bg-obsidian-900 border border-teal-500/20">
          <div className="flex items-center gap-2 text-teal-400 font-bold text-xs uppercase tracking-wider mb-3">
            <span className="p-1 rounded bg-teal-500/20">🌱</span>
            <span>Emerging</span>
          </div>
          <p className="text-[11px] text-slate-400 mb-3 leading-relaxed">
            High theoretical research volume; practical open-source codebases still forming.
          </p>
          <div className="space-y-2">
            {emerging.length > 0 ? (
              emerging.slice(0, 3).map((d) => (
                <div key={d.domain} className="p-2 rounded-lg bg-obsidian-850 border border-slate-800 text-xs">
                  <p className="font-semibold text-slate-200 truncate">{d.domain}</p>
                  <div className="flex items-center justify-between text-[10px] text-slate-400 mt-1">
                    <span className="font-mono text-teal-400">Ratio: {d.hype_adoption_ratio}x</span>
                    <span className="text-amber-400 flex items-center gap-0.5">
                      <AlertTriangle className="w-2.5 h-2.5" /> High Hype
                    </span>
                  </div>
                </div>
              ))
            ) : (
              <p className="text-slate-500 text-xs italic">No domains currently in emerging quadrant.</p>
            )}
          </div>
        </div>

        {/* Quadrant 2: Rising */}
        <div className="p-4 rounded-xl bg-obsidian-900 border border-emerald-500/20">
          <div className="flex items-center gap-2 text-emerald-400 font-bold text-xs uppercase tracking-wider mb-3">
            <Rocket className="w-3.5 h-3.5" />
            <span>Rising</span>
          </div>
          <p className="text-[11px] text-slate-400 mb-3 leading-relaxed">
            Balanced academic publications and rapid GitHub star velocity.
          </p>
          <div className="space-y-2">
            {rising.length > 0 ? (
              rising.slice(0, 3).map((d) => (
                <div key={d.domain} className="p-2 rounded-lg bg-obsidian-850 border border-slate-800 text-xs">
                  <p className="font-semibold text-slate-200 truncate">{d.domain}</p>
                  <div className="flex items-center justify-between text-[10px] text-slate-400 mt-1">
                    <span className="font-mono text-emerald-400">+{Math.round((d.wow_delta || 0.1) * 100)}% WoW</span>
                    <span className="font-mono text-slate-400">Impact: {d.avg_impact}/10</span>
                  </div>
                </div>
              ))
            ) : (
              <p className="text-slate-500 text-xs italic">No domains currently in rising quadrant.</p>
            )}
          </div>
        </div>

        {/* Quadrant 3: Established */}
        <div className="p-4 rounded-xl bg-obsidian-900 border border-blue-500/20">
          <div className="flex items-center gap-2 text-blue-400 font-bold text-xs uppercase tracking-wider mb-3">
            <Landmark className="w-3.5 h-3.5" />
            <span>Established</span>
          </div>
          <p className="text-[11px] text-slate-400 mb-3 leading-relaxed">
            Standard production toolchains with high cumulative star counts.
          </p>
          <div className="space-y-2">
            {established.length > 0 ? (
              established.slice(0, 3).map((d) => (
                <div key={d.domain} className="p-2 rounded-lg bg-obsidian-850 border border-slate-800 text-xs">
                  <p className="font-semibold text-slate-200 truncate">{d.domain}</p>
                  <div className="flex items-center justify-between text-[10px] text-slate-400 mt-1">
                    <span className="font-mono text-blue-400">{d.item_count} items</span>
                    <span className="text-slate-400">Stable</span>
                  </div>
                </div>
              ))
            ) : (
              <p className="text-slate-500 text-xs italic">No domains currently in established quadrant.</p>
            )}
          </div>
        </div>

        {/* Quadrant 4: Declining */}
        <div className="p-4 rounded-xl bg-obsidian-900 border border-rose-500/20">
          <div className="flex items-center gap-2 text-rose-400 font-bold text-xs uppercase tracking-wider mb-3">
            <TrendingDown className="w-3.5 h-3.5" />
            <span>Declining</span>
          </div>
          <p className="text-[11px] text-slate-400 mb-3 leading-relaxed">
            Subfields experiencing negative volume deltas or superseded by newer architectures.
          </p>
          <div className="space-y-2">
            {declining.length > 0 ? (
              declining.slice(0, 3).map((d) => (
                <div key={d.domain} className="p-2 rounded-lg bg-obsidian-850 border border-slate-800 text-xs">
                  <p className="font-semibold text-slate-200 truncate">{d.domain}</p>
                  <div className="flex items-center justify-between text-[10px] text-rose-400 mt-1">
                    <span>{Math.round((d.wow_delta || -0.1) * 100)}% WoW</span>
                    <span className="text-slate-500">Declining</span>
                  </div>
                </div>
              ))
            ) : (
              <p className="text-slate-500 text-xs italic">No domains currently in declining quadrant.</p>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
