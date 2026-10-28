import React from "react";
import { Database } from "lucide-react";

export function MetadataTable({ item }) {
  const meta = item.metadata || {};

  const rows = [
    { label: "Canonical Source", value: item.source.toUpperCase() },
    { label: "Original Identifier", value: item.source_id },
    { label: "Primary Category", value: item.primary_domain },
    { label: "Publication Date", value: item.created_at ? new Date(item.created_at).toLocaleDateString() : "N/A" },
  ];

  if (item.source === "arxiv") {
    rows.push(
      { label: "Total Citations", value: meta.citation_count || 0 },
      { label: "Influential Citations", value: meta.influential_citation_count || 0 },
      { label: "Max Author h-Index", value: meta.max_h_index || 0 },
      { label: "Code Linked in Abstract", value: meta.has_code ? "Yes (Verified GitHub link)" : "None" }
    );
  } else if (item.source === "github") {
    rows.push(
      { label: "Stargazers Count", value: meta.stargazers_count?.toLocaleString() || 0 },
      { label: "Forks Count", value: meta.forks_count?.toLocaleString() || 0 },
      { label: "Open Issues", value: meta.open_issues_count || 0 },
      { label: "Primary Language", value: meta.language || "Python" },
      { label: "Software License", value: meta.license || "None" }
    );
  } else {
    rows.push(
      { label: "HN Upvotes", value: meta.points || 0 },
      { label: "Comment Count", value: meta.num_comments || 0 },
      { label: "Submitting Author", value: meta.author || "anonymous" }
    );
  }

  return (
    <div className="glass-panel p-6 rounded-2xl">
      <div className="flex items-center gap-2 text-slate-300 font-bold text-xs uppercase tracking-wider mb-4">
        <Database className="w-4 h-4 text-emerald-400" />
        <span>Canonical Source Metadata</span>
      </div>

      <div className="divide-y divide-slate-800 text-xs">
        {rows.map((r, idx) => (
          <div key={idx} className="py-2.5 flex items-center justify-between">
            <span className="text-slate-400">{r.label}</span>
            <span className="font-mono text-slate-200 font-medium">{r.value}</span>
          </div>
        ))}
      </div>
    </div>
  );
}
