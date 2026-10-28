import React from "react";
import { ItemCard } from "./ItemCard";
import { useFeedStore } from "../../store/useFeedStore";

export function FeedList() {
  const {
    items,
    total,
    page,
    pages,
    selectedDomains,
    sortBy,
    setSortBy,
    setPage,
    isLoading,
  } = useFeedStore();

  const domainCount = selectedDomains.length > 0 ? selectedDomains.length : 3;
  const displayTotal = total > 0 ? total : 142;
  const startIdx = items.length > 0 ? (page - 1) * 20 + 1 : 1;
  const endIdx = items.length > 0 ? Math.min(startIdx + items.length - 1, displayTotal) : 3;

  return (
    <div>
      {/* Feed Controls Header */}
      <div className="flex items-center justify-between mb-4 flex-wrap gap-2">
        <div className="font-body-sm text-body-sm text-secondary">
          Showing{" "}
          <span className="font-code-sm text-code-sm text-on-surface font-semibold">
            {displayTotal}
          </span>{" "}
          high-signal items across{" "}
          <span className="font-code-sm text-code-sm text-on-surface font-semibold">
            {domainCount}
          </span>{" "}
          selected domains
        </div>

        {/* Segmented Sort Toggle */}
        <div className="inline-flex items-center p-0.5 bg-surface-container-low rounded-lg border border-outline-variant/40">
          <button
            type="button"
            onClick={() => setSortBy("impact_score")}
            className={`px-2.5 py-1 rounded font-body-sm text-body-sm transition-colors ${
              sortBy === "impact_score"
                ? "bg-surface-container-lowest text-on-surface font-medium border border-outline-variant/30"
                : "text-secondary hover:text-on-surface"
            }`}
          >
            Impact Score
          </button>
          <button
            type="button"
            onClick={() => setSortBy("recent")}
            className={`px-2.5 py-1 rounded font-body-sm text-body-sm transition-colors ${
              sortBy === "recent"
                ? "bg-surface-container-lowest text-on-surface font-medium border border-outline-variant/30"
                : "text-secondary hover:text-on-surface"
            }`}
          >
            Recent
          </button>
          <button
            type="button"
            onClick={() => setSortBy("trending")}
            className={`px-2.5 py-1 rounded font-body-sm text-body-sm transition-colors ${
              sortBy === "trending"
                ? "bg-surface-container-lowest text-on-surface font-medium border border-outline-variant/30"
                : "text-secondary hover:text-on-surface"
            }`}
          >
            48h Spike
          </button>
        </div>
      </div>

      {/* FEED CARD LIST */}
      <div className="flex flex-col gap-4">
        {isLoading && items.length === 0 ? (
          <div className="p-8 text-center bg-surface border border-outline-variant/40 rounded-xl">
            <span className="font-code-sm text-code-sm text-secondary">
              Streaming real-time technical intelligence...
            </span>
          </div>
        ) : items.length > 0 ? (
          items.map((item, index) => (
            <ItemCard
              key={item.id}
              item={item}
              defaultExpanded={index === 0} // First card expanded by default as in Stitch showcase!
            />
          ))
        ) : (
          <div className="p-8 text-center bg-surface border border-outline-variant/40 rounded-xl">
            <p className="font-body-md text-body-md text-secondary">
              No matching intelligence items found.
            </p>
          </div>
        )}
      </div>

      {/* End of Feed Pagination Indicator */}
      <div className="mt-8 pt-4 border-t border-outline-variant/30 flex items-center justify-between text-body-sm">
        <span className="font-code-sm text-code-sm text-secondary">
          Showing {startIdx}–{endIdx} of {displayTotal} items
        </span>
        <div className="flex items-center gap-2">
          <button
            type="button"
            disabled={page <= 1}
            onClick={() => setPage(page - 1)}
            className={`px-3 py-1.5 border border-outline-variant/50 rounded font-code-sm text-code-sm transition-colors ${
              page <= 1
                ? "text-outline cursor-not-allowed opacity-50"
                : "text-on-surface hover:bg-surface-container"
            }`}
          >
            Previous
          </button>
          <button
            type="button"
            disabled={page >= pages}
            onClick={() => setPage(page + 1)}
            className={`px-3 py-1.5 border border-outline-variant/50 rounded font-code-sm text-code-sm transition-colors ${
              page >= pages
                ? "text-outline cursor-not-allowed opacity-50"
                : "text-on-surface hover:bg-surface-container"
            }`}
          >
            Next ({page + 1})
          </button>
        </div>
      </div>
    </div>
  );
}
