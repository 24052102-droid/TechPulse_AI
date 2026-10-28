import React from "react";
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  Legend,
} from "recharts";

export function WeeklyComparisonBarChart({ domains = [] }) {
  const chartData = domains.slice(0, 7).map((d) => {
    const current = d.item_count || 10;
    const wow = d.wow_delta || 0.1;
    const previous = Math.max(1, Math.round(current / (1 + wow)));
    return {
      domain: d.domain.length > 14 ? d.domain.substring(0, 12) + "..." : d.domain,
      current,
      previous,
    };
  });

  return (
    <div className="glass-panel p-5 rounded-2xl">
      <div className="flex items-center justify-between mb-4">
        <div>
          <h3 className="text-sm font-bold text-slate-100">Week-over-Week Volume Delta</h3>
          <p className="text-xs text-slate-400">Current week vs. prior 7-day baseline</p>
        </div>
      </div>

      <div className="h-64 w-full">
        <ResponsiveContainer width="100%" height="100%">
          <BarChart data={chartData} margin={{ top: 10, right: 10, left: -20, bottom: 0 }}>
            <CartesianGrid strokeDasharray="3 3" stroke="#1D283E" />
            <XAxis dataKey="domain" stroke="#64748B" fontSize={11} tickLine={false} />
            <YAxis stroke="#64748B" fontSize={11} tickLine={false} />
            <Tooltip
              contentStyle={{
                backgroundColor: "#0D131F",
                borderColor: "#2B3A56",
                borderRadius: "12px",
                fontSize: "12px",
              }}
            />
            <Legend wrapperStyle={{ fontSize: "11px", paddingTop: "8px" }} />
            <Bar dataKey="current" name="This Week" fill="#10B981" radius={[4, 4, 0, 0]} />
            <Bar dataKey="previous" name="Prior Week" fill="#3B82F6" radius={[4, 4, 0, 0]} />
          </BarChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
}
