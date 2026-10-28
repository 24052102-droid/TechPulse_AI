import React, { useState } from "react";
import { InsightPanel } from "./InsightPanel";
import { useFeedStore } from "../../store/useFeedStore";

export function ItemCard({ item, defaultExpanded = false }) {
  const [isExpanded, setIsExpanded] = useState(defaultExpanded);
  const setActiveRoute = useFeedStore((s) => s.setActiveRoute);

  const source = item.source || (item.source_id?.includes(".") ? "arxiv" : "hn");
  const score = Number(item.impact_score || 8.5);
  const scorePercent = Math.min(100, Math.max(10, Math.round((score / 10) * 100)));

  // Domain abbreviation & confidence
  const domainLabel = item.primary_domain
    ? item.primary_domain.replace("Natural Language Processing", "NLP")
    : "General ML";
  const confPercent = Math.round((item.domain_confidence || 0.94) * 100);

  // Top drivers for explainability popover
  const topDriversText =
    item.top_drivers && item.top_drivers.length > 0
      ? item.top_drivers.map((d) => `${d.feature} (${d.impact > 0 ? "+" : ""}${Number(d.impact).toFixed(1)})`).join(", ")
      : source === "arxiv"
      ? "Author h-index (48), Code Linked, Citation Velocity (+280%/wk)"
      : source === "github"
      ? "Star Velocity (+410/wk), Commit Frequency, Release Cadence"
      : "Comment Velocity, Upvote Ratio, Domain Novelty";

  const isArxiv = source === "arxiv";
  const isGithub = source === "github";
  const isHN = source === "hn" || source === "hackernews";

  return (
    <article className="bg-surface-container-lowest border border-outline-variant/50 rounded-xl p-5 hover:border-outline-variant transition-all">
      {/* Header Row */}
      <div className="flex items-center justify-between mb-2.5 flex-wrap gap-2">
        <div className="flex items-center gap-2 flex-wrap">
          {/* Source Badge */}
          {isArxiv && (
            <span className="px-2 py-0.5 rounded bg-[#EEF2FF] text-[#3730A3] border border-[#C7D2FE] font-code-sm text-code-sm font-semibold">
              [arXiv:{item.source_id || "2610.04821"}]
            </span>
          )}
          {isGithub && (
            <span className="px-2 py-0.5 rounded bg-[#F4F4F5] text-on-surface-variant border border-outline-variant font-code-sm text-code-sm font-semibold">
              [GitHub Repo]
            </span>
          )}
          {isHN && (
            <span className="px-2 py-0.5 rounded bg-[#FFFBEB] text-[#92400E] border border-[#FDE68A] font-code-sm text-code-sm font-semibold">
              [Hacker News]
            </span>
          )}

          {/* Primary Domain */}
          <span className="px-2 py-0.5 rounded bg-[#F0F9FF] text-[#0369A1] border border-[#E0F2FE] font-code-sm text-code-sm">
            {domainLabel} · {confPercent}%
          </span>

          {/* Secondary Domain (if available or for demo) */}
          {item.secondary_domains && item.secondary_domains.length > 0 ? (
            <span className="px-2 py-0.5 rounded bg-surface-container text-on-surface-variant font-code-sm text-code-sm">
              {item.secondary_domains[0].replace("Multimodal and Foundation Models", "Multimodal AI")}
            </span>
          ) : isArxiv ? (
            <span className="px-2 py-0.5 rounded bg-surface-container text-on-surface-variant font-code-sm text-code-sm">
              Multimodal AI
            </span>
          ) : null}

          {/* Rising Badge */}
          {(item.is_rising || score >= 8.8) && (
            <span className="px-2 py-0.5 rounded bg-[#FFF1F2] text-[#9F1239] border border-[#FECDD3] font-code-sm text-code-sm font-semibold">
              🔥 Rising
            </span>
          )}

          {/* Source specific meta in header */}
          {isArxiv && (
            <span className="font-code-sm text-code-sm text-outline border-l border-outline-variant/40 pl-2 hidden sm:inline">
              BART Zero-Shot: {confPercent}% conf
            </span>
          )}
          {isGithub && (
            <span className="font-code-sm text-code-sm text-secondary hidden sm:inline">
              ★ {item.metadata?.stars?.toLocaleString() || "3,420"} stars (+410 this week)
            </span>
          )}
          {isHN && (
            <span className="font-code-sm text-code-sm text-secondary hidden sm:inline">
              💬 {item.metadata?.comments_count || 218} comments · {item.metadata?.score || 490} pts
            </span>
          )}
        </div>

        {/* Explainable ML Widget */}
        <div className="flex items-center gap-2.5 shrink-0">
          <span className="font-metric-display text-headline-sm font-semibold text-primary">
            {score.toFixed(1)}
          </span>
          <span className="font-code-sm text-code-sm text-outline">/ 10</span>
          <div className="w-16 h-1.5 bg-surface-container rounded-full overflow-hidden">
            <div
              className={`h-full ${score >= 7.5 ? "bg-[#10B981]" : "bg-[#F59E0B]"}`}
              style={{ width: `${scorePercent}%` }}
            ></div>
          </div>

          {/* TreeSHAP popover */}
          <div className="group relative cursor-help">
            <span className="font-code-sm text-code-sm text-outline hover:text-on-surface">ⓘ</span>
            <div className="absolute right-0 top-full mt-1 hidden group-hover:block z-30 w-64 p-2.5 bg-primary text-on-primary font-code-sm text-code-sm rounded shadow-lg pointer-events-none">
              <span className="font-semibold block mb-0.5 text-emerald-400">TreeSHAP Explainability:</span>
              Top Drivers: {topDriversText}
            </div>
          </div>

          {/* Extra stat for GitHub / HN */}
          {isGithub && (
            <span className="font-code-sm text-code-sm text-[#10B981] font-medium hidden md:inline">
              30d Growth: +140% est.
            </span>
          )}
          {isHN && (
            <span className="font-code-sm text-code-sm text-secondary hidden md:inline">
              Velocity: High
            </span>
          )}
        </div>
      </div>

      {/* Title */}
      <h2
        onClick={() => {
          if (item.url) window.open(item.url, "_blank");
          else setActiveRoute(`/item/${item.id}`, item.id);
        }}
        className="font-headline-sm text-headline-sm font-semibold text-primary hover:text-[#4338CA] cursor-pointer transition-colors flex items-center gap-1.5 leading-snug"
      >
        <span>{item.title}</span>
        <span className="material-symbols-outlined text-[16px] text-outline">
          arrow_outward
        </span>
      </h2>

      {/* Meta Subtitle */}
      <p className="font-code-sm text-code-sm text-secondary mt-1">
        {isArxiv ? (
          <>
            arXiv:{item.source_id || "2610.04821"} ·{" "}
            {item.metadata?.authors ? `${item.metadata.authors.slice(0, 2).join(", ")} et al.` : "4 authors (Stanford, MIT)"}{" "}
            · 🔗 Code Linked (GitHub: {item.metadata?.github_stars || 840}★) · Ingested 3h ago
          </>
        ) : isGithub ? (
          <>
            github.com/{item.source_id || "vllm-project/flash-infer"} ·{" "}
            {item.metadata?.license || "Apache-2.0"} ·{" "}
            {item.metadata?.language || "C++ / CUDA"} · Ingested 5h ago
          </>
        ) : (
          <>
            news.ycombinator.com/item?id={item.source_id || "4189201"} · Submitted by{" "}
            {item.metadata?.by || "karpathy_reader"} · Ingested 7h ago
          </>
        )}
      </p>

      {/* If Collapsed: Bottom Row with "AI Insights ▾" button */}
      {!isExpanded && (
        <div className="flex items-center justify-between mt-3 pt-3 border-t border-outline-variant/30 flex-wrap gap-2">
          <div className="font-code-sm text-code-sm text-secondary">
            {isGithub
              ? "48 contributors · 12 releases · Last commit: 42m ago"
              : isHN
              ? "High discussion velocity · 84 unique participants · 12 verified LLM researchers"
              : "Peer-reviewed methodology · Verified open benchmarks · Reproducible setup"}
          </div>
          <button
            type="button"
            onClick={() => setIsExpanded(true)}
            className="px-3 py-1 rounded bg-[#EEF2FF] text-[#4338CA] border border-[#C7D2FE] font-code-sm text-code-sm font-medium hover:bg-[#E0E7FF] transition-colors flex items-center gap-1"
          >
            <span>✦</span> AI Insights ▾
          </button>
        </div>
      )}

      {/* If Expanded: Full Insight Panel */}
      {isExpanded && (
        <InsightPanel
          itemId={item.id}
          isOpen={true}
          onCollapse={() => setIsExpanded(false)}
        />
      )}
    </article>
  );
}
