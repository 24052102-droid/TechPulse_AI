import React, { useState, useEffect } from "react";
import { api } from "../../api/client";
import { useFeedStore } from "../../store/useFeedStore";

export function InsightPanel({ itemId, isOpen, onCollapse, fallbackContent }) {
  const setActiveRoute = useFeedStore((s) => s.setActiveRoute);
  const [insight, setInsight] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  useEffect(() => {
    if (!isOpen) return;

    let isMounted = true;
    let pollInterval = null;

    async function loadInsight() {
      setLoading(true);
      setError(null);
      try {
        const res = await api.getInsights(itemId);
        if (res.status === "ready" && isMounted) {
          setInsight(res.insight);
          setLoading(false);
        } else if (res.status === "processing") {
          let attempts = 0;
          pollInterval = setInterval(async () => {
            attempts++;
            if (attempts > 8) {
              clearInterval(pollInterval);
              if (isMounted) {
                setError("Insight synthesis took too long. Click to retry.");
                setLoading(false);
              }
              return;
            }
            try {
              const pollRes = await api.getInsights(itemId);
              if (pollRes.status === "ready" && isMounted) {
                setInsight(pollRes.insight);
                setLoading(false);
                clearInterval(pollInterval);
              } else if (pollRes.status === "failed" && isMounted) {
                setError("Insight generation could not be completed for this item.");
                setLoading(false);
                clearInterval(pollInterval);
              }
            } catch (pErr) {
              clearInterval(pollInterval);
              if (isMounted) {
                setError("Connection lost while waiting for insights.");
                setLoading(false);
              }
            }
          }, 2500);
        } else if (fallbackContent && isMounted) {
          setInsight(fallbackContent);
          setLoading(false);
        } else if (isMounted) {
          setError("Insight generation status: " + (res.status || "unavailable"));
          setLoading(false);
        }
      } catch (err) {
        if (fallbackContent && isMounted) {
          setInsight(fallbackContent);
          setLoading(false);
        } else if (isMounted) {
          setError("AI synthesis streaming is currently unavailable.");
          setLoading(false);
        }
      }
    }

    loadInsight();

    return () => {
      isMounted = false;
      if (pollInterval) clearInterval(pollInterval);
    };
  }, [isOpen, itemId, fallbackContent]);

  if (!isOpen) return null;

  // Use fetched insight or passed-in fallback; show loading/error if neither is available
  const content = insight || fallbackContent || null;

  if (!content && !loading) {
    return (
      <div className="mt-4 pt-4 border-t border-dashed border-outline-variant/60 bg-surface -mx-5 -mb-5 p-5 rounded-b-xl">
        <p className="font-body-sm text-body-sm text-secondary italic">
          {error || "AI insights are not yet available for this item. Click to retry."}
        </p>
        <button
          type="button"
          onClick={onCollapse}
          className="mt-2 px-2.5 py-1 rounded bg-primary text-on-primary font-code-sm text-code-sm font-medium hover:bg-surface-tint transition-colors flex items-center gap-1"
        >
          <span>✦</span> Collapse Insights ▴
        </button>
      </div>
    );
  }

  if (!content) {
    // Still loading — will render the skeleton below
  }

  const depthLabel = content
    ? content.technical_depth?.includes("Depth")
      ? content.technical_depth
      : `${content.technical_depth || "Intermediate"} Depth`
    : "Loading…";

  return (
    <div className="mt-4 pt-4 border-t border-dashed border-outline-variant/60 bg-surface -mx-5 -mb-5 p-5 rounded-b-xl">
      {/* Meta Bar */}
      {content && (
      <div className="flex items-center justify-between mb-3 text-body-sm flex-wrap gap-2">
        <div className="flex items-center gap-2">
          <span className="px-2 py-0.5 rounded bg-[#F5F3FF] text-[#5B21B6] border border-[#DDD6FE] font-code-sm text-code-sm font-semibold capitalize">
            {depthLabel}
          </span>
          <span className="font-code-sm text-code-sm text-secondary">
            Est. Read: {content.estimated_read_time || 8} min
          </span>
        </div>
        <div className="flex items-center gap-1.5 font-code-sm text-code-sm text-secondary">
          <span className="w-1.5 h-1.5 rounded-full bg-[#8B5CF6]"></span>
          <span>{content.llm_model ? `${content.llm_model} Synthesis` : "AI Synthesis"}</span>
        </div>
      </div>
      )}

      {loading && !content ? (
        <div className="py-4 space-y-2 animate-pulse">
          <div className="h-3.5 bg-surface-container rounded w-5/6"></div>
          <div className="h-3.5 bg-surface-container rounded w-4/6"></div>
        </div>
      ) : (
        <>
          {/* 3-Sentence Summary */}
          <p className="font-body-md text-body-md text-on-surface leading-relaxed mb-3">
            {content.summary}
          </p>

          {/* Key Technical Takeaways */}
          {content.key_takeaways && content.key_takeaways.length > 0 && (
            <div className="space-y-1.5 mb-3 font-body-sm text-body-sm text-on-surface">
              {content.key_takeaways.map((takeaway, idx) => (
                <div key={idx} className="flex items-start gap-2">
                  <span className="font-code-sm text-code-sm text-[#4338CA] mt-0.5">▪</span>
                  <span>{takeaway}</span>
                </div>
              ))}
            </div>
          )}

          {/* Strategic Relevance Callout */}
          {content.why_it_matters && (
            <div className="border-l-[3px] border-[#6366F1] bg-[#EEF2FF] p-3 rounded-r font-body-sm text-body-sm text-[#1E1B4B] leading-relaxed">
              <span className="font-semibold block mb-0.5 font-code-sm text-code-sm uppercase tracking-wide text-[#3730A3]">
                Strategic Relevance
              </span>
              {content.why_it_matters}
            </div>
          )}

          {/* Footer Row */}
          <div className="flex items-center justify-between mt-4 pt-3 border-t border-outline-variant/30 flex-wrap gap-2">
            <div className="flex items-center gap-1.5 flex-wrap">
              {(content.related_topics || []).map(
                (topic, idx) => (
                  <span
                    key={idx}
                    className="font-code-sm text-code-sm text-secondary bg-surface-container px-2 py-0.5 rounded"
                  >
                    #{topic.replace("#", "")}
                  </span>
                )
              )}
            </div>

            <div className="flex items-center gap-3">
              <button
                type="button"
                onClick={() => setActiveRoute(`/item/${itemId}`, itemId)}
                className="font-body-sm text-body-sm text-primary font-medium underline underline-offset-2 hover:text-[#4338CA] transition-colors"
              >
                Open Full Deep-Dive &amp; ML Forecast →
              </button>
              <button
                type="button"
                onClick={onCollapse}
                className="px-2.5 py-1 rounded bg-primary text-on-primary font-code-sm text-code-sm font-medium hover:bg-surface-tint transition-colors flex items-center gap-1"
              >
                <span>✦</span> Collapse Insights ▴
              </button>
            </div>
          </div>
        </>
      )}
    </div>
  );
}
