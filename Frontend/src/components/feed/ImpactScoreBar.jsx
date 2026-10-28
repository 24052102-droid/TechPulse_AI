import React, { useState } from "react";
import { Info, Sparkles, TrendingUp } from "lucide-react";

export function ImpactScoreBar({ score, topDrivers = [], source = "arxiv" }) {
  const [showPopover, setShowPopover] = useState(false);
  const displayScore = Number(score || 5.0).toFixed(1);
  const scorePercent = Math.min(100, Math.max(0, (displayScore / 10.0) * 100));

  let colorCls = "bg-impact-rose text-rose-400 border-rose-500/30";
  let barColor = "bg-rose-500";
  let tierLabel = "Baseline Cohort";

  if (displayScore >= 7.5) {
    colorCls = "bg-impact-emerald/10 text-emerald-400 border-emerald-500/30";
    barColor = "bg-emerald-500";
    tierLabel = "Top Decile (Viral Signal)";
  } else if (displayScore >= 4.0) {
    colorCls = "bg-impact-amber/10 text-amber-400 border-amber-500/30";
    barColor = "bg-amber-500";
    tierLabel = "Moderate Growth Cohort";
  }

  const horizonText =
    source === "arxiv"
      ? "Target: 180-day Normalized Citations"
      : source === "github"
      ? "Target: 30-day Star Velocity"
      : "Target: Discussion Velocity";

  return (
    <div
      className="relative inline-flex items-center gap-2"
      onMouseEnter={() => setShowPopover(true)}
      onMouseLeave={() => setShowPopover(false)}
    >
      <div className="flex items-center gap-1.5 cursor-pointer">
        <span className="text-xs font-semibold text-slate-300">Impact:</span>
        <span className={`px-2 py-0.5 rounded text-xs font-mono font-bold border ${colorCls}`}>
          {displayScore}/10
        </span>
      </div>

      {/* Mini Progress Bar */}
      <div className="w-16 h-2 bg-obsidian-800 rounded-full overflow-hidden border border-slate-700/50 hidden sm:block">
        <div
          className={`h-full ${barColor} transition-all duration-300 rounded-full`}
          style={{ width: `${scorePercent}%` }}
        />
      </div>

      <button className="text-slate-400 hover:text-slate-200" title="Inspect TreeSHAP feature attributions">
        <Info className="w-3.5 h-3.5 opacity-70" />
      </button>

      {/* Explainable Popover on Hover (F-03) */}
      {showPopover && (
        <div className="absolute z-40 bottom-full right-0 mb-2 w-72 p-3 rounded-xl bg-obsidian-900/95 backdrop-blur-md border border-slate-700/80 shadow-2xl text-xs text-slate-200">
          <div className="flex items-center justify-between pb-2 border-b border-slate-800 mb-2">
            <div className="flex items-center gap-1 text-emerald-400 font-semibold">
              <Sparkles className="w-3.5 h-3.5" />
              <span>TreeSHAP Model Explainability</span>
            </div>
            <span className="text-[10px] text-slate-400 font-mono">XGBoost v1.0</span>
          </div>

          <p className="text-[11px] text-slate-300 font-medium mb-1">
            Status: <span className="text-white">{tierLabel}</span>
          </p>
          <p className="text-[10px] text-slate-400 mb-2">{horizonText}</p>

          <p className="text-[11px] font-semibold text-slate-200 mb-1.5 flex items-center gap-1">
            <TrendingUp className="w-3 h-3 text-emerald-400" />
            <span>Top 3 Feature Drivers:</span>
          </p>

          <div className="space-y-1.5">
            {topDrivers && topDrivers.length > 0 ? (
              topDrivers.map((driver, idx) => {
                const impactVal = Number(driver.impact || 0);
                const isPositive = impactVal >= 0;
                return (
                  <div
                    key={idx}
                    className="flex items-center justify-between px-2 py-1 rounded bg-obsidian-850 border border-slate-800/80 font-mono text-[11px]"
                  >
                    <span className="text-slate-300 truncate max-w-[170px]" title={driver.feature}>
                      {idx + 1}. {driver.feature}
                    </span>
                    <span
                      className={`font-semibold ${
                        isPositive ? "text-emerald-400" : "text-rose-400"
                      }`}
                    >
                      {isPositive ? "+" : ""}
                      {impactVal.toFixed(2)}
                    </span>
                  </div>
                );
              })
            ) : (
              <p className="text-slate-400 text-[10px]">No feature attributions recorded.</p>
            )}
          </div>
        </div>
      )}
    </div>
  );
}
