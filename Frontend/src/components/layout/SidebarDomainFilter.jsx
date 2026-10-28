import React, { useEffect } from "react";
import { useFeedStore } from "../../store/useFeedStore";

export function SidebarDomainFilter() {
  const {
    selectedSource,
    setSelectedSource,
    domainsData,
    selectedDomains,
    toggleDomain,
    clearDomains,
    loadDomains,
  } = useFeedStore();

  useEffect(() => {
    loadDomains();
  }, [loadDomains]);

  // Fallback / standard taxonomy with canonical domain mappings
  const defaultTaxonomy = [
    { label: "Natural Language", key: "Natural Language Processing", count: 142 },
    { label: "Computer Vision", key: "Computer Vision", count: 98 },
    { label: "Multimodal AI", key: "Multimodal and Foundation Models", count: 64 },
    { label: "Systems & Infra", key: "Systems and Infrastructure", count: 51 },
    { label: "Reinforcement Learning", key: "Reinforcement Learning", count: 29 },
    { label: "General ML", key: "General Machine Learning", count: 88 },
    { label: "Data Engineering", key: "Data Engineering and Pipelines", count: 31 },
    { label: "Security", key: "Security and Privacy", count: 24 },
    { label: "Robotics", key: "Robotics", count: 19 },
    { label: "IoT & Embedded", key: "IoT and Embedded Systems", count: 15 },
  ];

  // Merge dynamic counts from domainsData if available
  const taxonomy = defaultTaxonomy.map((item) => {
    const live = (domainsData || []).find(
      (d) =>
        d.domain === item.key ||
        d.domain.toLowerCase() === item.label.toLowerCase() ||
        d.domain.toLowerCase().includes(item.label.toLowerCase())
    );
    return {
      ...item,
      count: live?.item_count || item.count,
    };
  });

  const sourceNodes = [
    { id: "all", label: "All Sources", dotColor: null, count: 284 },
    { id: "arxiv", label: "arXiv Papers", dotColor: "#6366F1", count: 142 },
    { id: "github", label: "GitHub Repos", dotColor: "#c8c5ca", count: 98 },
    { id: "hn", label: "Hacker News", dotColor: "#F59E0B", count: 44 },
  ];

  return (
    <aside className="w-[240px] shrink-0 bg-surface border-r border-outline-variant/40 min-h-[calc(100vh-100px)] p-5 select-none">
      {/* Section 1: SOURCE */}
      <div className="mb-6">
        <div className="flex items-center justify-between mb-2.5">
          <span className="font-label-caps text-label-caps uppercase tracking-wider text-outline font-semibold">
            Source
          </span>
          <span className="font-code-sm text-code-sm text-outline">4 nodes</span>
        </div>
        <div className="flex flex-col gap-1">
          {sourceNodes.map((s) => {
            const isActive = selectedSource === s.id;
            return (
              <button
                key={s.id}
                onClick={() => setSelectedSource(s.id)}
                className={`w-full flex items-center justify-between px-2.5 py-1.5 rounded font-body-sm text-body-sm transition-colors text-left group ${
                  isActive
                    ? "bg-primary text-on-primary font-medium tracking-tight"
                    : "bg-transparent hover:bg-surface-container text-on-surface"
                }`}
                type="button"
              >
                <span className="flex items-center gap-2">
                  {s.dotColor ? (
                    <span
                      className="w-1.5 h-1.5 rounded-full"
                      style={{ backgroundColor: s.dotColor }}
                    ></span>
                  ) : null}
                  <span>{s.label}</span>
                </span>
                <span
                  className={`font-code-sm text-code-sm rounded px-1.5 py-0.5 ${
                    isActive
                      ? "bg-white/20 text-on-primary"
                      : "text-secondary group-hover:text-on-surface"
                  }`}
                >
                  {s.count}
                </span>
              </button>
            );
          })}
        </div>
      </div>

      {/* Section 2: DOMAINS (10) */}
      <div>
        <div className="flex items-center justify-between mb-3 pt-4 border-t border-outline-variant/40">
          <span className="font-label-caps text-label-caps uppercase tracking-wider text-outline font-semibold">
            Domains (10)
          </span>
          <button
            onClick={clearDomains}
            className="font-code-sm text-code-sm text-outline hover:text-primary transition-colors cursor-pointer"
            type="button"
          >
            Reset
          </button>
        </div>
        <div className="flex flex-col gap-1.5">
          {taxonomy.map((item) => {
            const isChecked = selectedDomains.includes(item.key);
            return (
              <label
                key={item.key}
                className="flex items-center justify-between px-2 py-1 rounded hover:bg-surface-container cursor-pointer group"
              >
                <div className="flex items-center gap-2 min-w-0">
                  <input
                    type="checkbox"
                    checked={isChecked}
                    onChange={() => toggleDomain(item.key)}
                    className="w-3.5 h-3.5 rounded border-outline-variant text-primary focus:ring-0 cursor-pointer accent-black"
                  />
                  <span className="font-body-sm text-body-sm text-on-surface truncate">
                    {item.label}
                  </span>
                </div>
                <span className="font-code-sm text-code-sm text-secondary group-hover:text-on-surface shrink-0 ml-1">
                  {item.count}
                </span>
              </label>
            );
          })}
        </div>
      </div>
    </aside>
  );
}
