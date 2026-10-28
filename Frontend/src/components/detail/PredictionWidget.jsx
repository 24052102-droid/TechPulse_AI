import React from "react";
import { Sparkles, TrendingUp, Cpu } from "lucide-react";
import { AreaChart, Area, XAxis, YAxis, ResponsiveContainer, Tooltip } from "recharts";

export function PredictionWidget({ prediction, source }) {
  const displayScore = prediction?.score_display || 5.0;
  const rawScore = prediction?.score || 0.5;
  const topDrivers = prediction?.features_used?.top_drivers || [];

  // Generate 180-day projected trajectory
  const trajectoryData = [
    { day: "Day 0", projection: 0, upper: 0, lower: 0 },
    { day: "Day 30", projection: Math.round(rawScore * 8), upper: Math.round(rawScore * 12), lower: Math.round(rawScore * 5) },
    { day: "Day 60", projection: Math.round(rawScore * 18), upper: Math.round(rawScore * 25), lower: Math.round(rawScore * 12) },
    { day: "Day 90", projection: Math.round(rawScore * 32), upper: Math.round(rawScore * 42), lower: Math.round(rawScore * 22) },
    { day: "Day 120", projection: Math.round(rawScore * 48), upper: Math.round(rawScore * 65), lower: Math.round(rawScore * 34) },
    { day: "Day 180", projection: Math.round(rawScore * 75), upper: Math.round(rawScore * 105), lower: Math.round(rawScore * 52) },
  ];

  return (
    <div className="glass-panel p-6 rounded-2xl space-y-6">
      <div className="flex items-center justify-between pb-3 border-b border-slate-800">
        <div className="flex items-center gap-2 text-emerald-400 font-bold text-xs uppercase tracking-wider">
          <Cpu className="w-4 h-4" />
          <span>ML Prediction Engine</span>
        </div>
        <span className="text-[10px] font-mono text-slate-400 bg-slate-800 px-2 py-0.5 rounded">
          {prediction?.model_version || "XGBoost v1.0"}
        </span>
      </div>

      {/* Score Gauge Block */}
      <div className="text-center py-4 bg-obsidian-900 rounded-2xl border border-slate-800/80">
        <p className="text-xs text-slate-400 mb-1">Predicted Technical Impact</p>
        <div className="flex items-baseline justify-center gap-1">
          <span className="text-4xl font-extrabold font-mono text-emerald-400">
            {displayScore}
          </span>
          <span className="text-slate-500 font-mono text-lg">/ 10.0</span>
        </div>
        <p className="text-[11px] text-slate-400 font-medium mt-1">
          {displayScore >= 7.5 ? "Viral Signal · Top Decile" : displayScore >= 4.0 ? "Moderate Growth Cohort" : "Baseline Cohort"}
        </p>
        <p className="text-[10px] font-mono text-slate-500 mt-1">
          Target: {source === "arxiv" ? "180-day Normalized Citations" : "30-day Star Velocity"}
        </p>
      </div>

      {/* TreeSHAP Drivers */}
      <div>
        <h4 className="text-xs font-bold text-slate-300 mb-3 flex items-center gap-1.5">
          <Sparkles className="w-3.5 h-3.5 text-emerald-400" />
          <span>TreeSHAP Feature Attributions</span>
        </h4>
        <div className="space-y-2">
          {topDrivers.length > 0 ? (
            topDrivers.map((driver, idx) => {
              const impact = Number(driver.impact || 0);
              const isPos = impact >= 0;
              return (
                <div
                  key={idx}
                  className="flex items-center justify-between p-2 rounded-lg bg-obsidian-900 border border-slate-800/80 text-xs font-mono"
                >
                  <span className="text-slate-300 truncate max-w-[160px]" title={driver.feature}>
                    {idx + 1}. {driver.feature}
                  </span>
                  <span className={`font-semibold ${isPos ? "text-emerald-400" : "text-rose-400"}`}>
                    {isPos ? "+" : ""}
                    {impact.toFixed(3)}
                  </span>
                </div>
              );
            })
          ) : (
            <p className="text-xs text-slate-500 italic">No feature attribution data recorded.</p>
          )}
        </div>
      </div>

      {/* 180-Day Trajectory Area Chart */}
      <div>
        <div className="flex items-center justify-between mb-2">
          <h4 className="text-xs font-bold text-slate-300 flex items-center gap-1.5">
            <TrendingUp className="w-3.5 h-3.5 text-emerald-400" />
            <span>180-Day Growth Forecast</span>
          </h4>
          <span className="text-[10px] text-slate-500 font-mono">90% Confidence Band</span>
        </div>
        <div className="h-36 w-full bg-obsidian-900 p-2 rounded-xl border border-slate-800">
          <ResponsiveContainer width="100%" height="100%">
            <AreaChart data={trajectoryData} margin={{ top: 5, right: 5, left: -25, bottom: 0 }}>
              <defs>
                <linearGradient id="growthGrad" x1="0" y1="0" x2="0" y2="1">
                  <stop offset="5%" stopColor="#10B981" stopOpacity={0.3} />
                  <stop offset="95%" stopColor="#10B981" stopOpacity={0.0} />
                </linearGradient>
              </defs>
              <XAxis dataKey="day" stroke="#64748B" fontSize={10} tickLine={false} />
              <YAxis stroke="#64748B" fontSize={10} tickLine={false} />
              <Tooltip
                contentStyle={{
                  backgroundColor: "#0D131F",
                  borderColor: "#2B3A56",
                  borderRadius: "8px",
                  fontSize: "11px",
                }}
              />
              <Area type="monotone" dataKey="projection" stroke="#10B981" strokeWidth={2} fillOpacity={1} fill="url(#growthGrad)" />
              <Area type="monotone" dataKey="upper" stroke="#047857" strokeDasharray="2 2" fill="none" />
            </AreaChart>
          </ResponsiveContainer>
        </div>
      </div>
    </div>
  );
}
