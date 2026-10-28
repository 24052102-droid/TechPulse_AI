import React from "react";
import { useFeedStore } from "../../store/useFeedStore";

export function TrendingBanner({ items = [] }) {
  const setActiveRoute = useFeedStore((s) => s.setActiveRoute);

  const fallbackItems = [
    { id: "fallback-1", title: "vLLM-FP8 Kernel Optimization", impact_score: 9.4 },
    { id: "fallback-2", title: "DeepSeek-V3 MoE Architecture", impact_score: 9.1 },
    { id: "fallback-3", title: "BitNet b1.58 Ternary Scaling", impact_score: 8.8 },
  ];

  const candidateItems = items
    .filter((i) => i.is_rising || (i.impact_score && i.impact_score >= 7.5))
    .slice(0, 3);

  const displayItems = candidateItems.length >= 3 ? candidateItems : fallbackItems;

  return (
    <div className="h-11 bg-surface border border-outline-variant/50 rounded-lg px-4 flex items-center justify-between text-body-sm mb-6">
      <div className="flex items-center gap-3 overflow-hidden">
        <span className="inline-flex items-center gap-1.5 px-2 py-0.5 rounded bg-[#FFF1F2] text-[#9F1239] border border-[#FECDD3] font-code-sm text-code-sm font-semibold shrink-0">
          <span>🔥</span> Rising 48h
        </span>
        <div className="flex items-center gap-3 overflow-x-auto whitespace-nowrap">
          {displayItems.map((item, idx) => (
            <React.Fragment key={item.id || idx}>
              {idx > 0 && <span className="text-outline-variant font-code-sm text-code-sm">/</span>}
              <span
                onClick={() => {
                  if (item.id && !item.id.startsWith("fallback")) {
                    setActiveRoute(`/item/${item.id}`, item.id);
                  }
                }}
                className="font-body-sm text-body-sm text-on-surface hover:text-[#4338CA] cursor-pointer transition-colors flex items-center gap-1.5"
              >
                <span className="truncate max-w-[240px]">{item.title}</span>
                <span className="font-code-sm text-code-sm bg-surface-container px-1 py-0.5 rounded text-secondary font-medium">
                  {Number(item.impact_score || 9.0).toFixed(1)}
                </span>
              </span>
            </React.Fragment>
          ))}
        </div>
      </div>
      <div className="font-code-sm text-code-sm text-secondary shrink-0 pl-3">
        Updated 12m ago
      </div>
    </div>
  );
}
