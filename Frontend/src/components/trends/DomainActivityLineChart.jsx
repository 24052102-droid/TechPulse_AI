import React from "react";
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
} from "recharts";

export function DomainActivityLineChart({ trends = [] }) {
  // Aggregate daily history by date and top domains
  const dateMap = {};
  trends.forEach((t) => {
    const dStr = t.date || "Today";
    if (!dateMap[dStr]) {
      dateMap[dStr] = { date: dStr };
    }
    dateMap[dStr][t.domain] = t.item_count;
  });

  const chartData = Object.values(dateMap).sort((a, b) => (a.date > b.date ? 1 : -1));

  const colors = [
    "#10B981", // Emerald
    "#3B82F6", // Blue
    "#A855F7", // Purple
    "#F59E0B", // Amber
    "#06B6D4", // Cyan
  ];

  const topDomains = [
    "Natural Language Processing",
    "Computer Vision",
    "General Machine Learning",
    "Systems and Infrastructure",
    "Reinforcement Learning",
  ];

  return (
    <div className="glass-panel p-5 rounded-2xl">
      <div className="flex items-center justify-between mb-4">
        <div>
          <h3 className="text-sm font-bold text-slate-100">Domain Velocity Over Time</h3>
          <p className="text-xs text-slate-400">Daily rolling intelligence volume across core subfields</p>
        </div>
      </div>

      <div className="h-64 w-full">
        <ResponsiveContainer width="100%" height="100%">
          <LineChart data={chartData} margin={{ top: 10, right: 10, left: -20, bottom: 0 }}>
            <CartesianGrid strokeDasharray="3 3" stroke="#1D283E" />
            <XAxis dataKey="date" stroke="#64748B" fontSize={11} tickLine={false} />
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
            {topDomains.map((dom, idx) => (
              <Line
                key={dom}
                type="monotone"
                dataKey={dom}
                stroke={colors[idx % colors.length]}
                strokeWidth={2}
                dot={{ r: 3 }}
                activeDot={{ r: 5 }}
              />
            ))}
          </LineChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
}
