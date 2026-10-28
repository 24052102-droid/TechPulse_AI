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
          setInsight(res.data);
          setLoading(false);
        } else if (res.status === "processing") {
          pollInterval = setInterval(async () => {
            try {
              const pollRes = await api.getInsights(itemId);
              if (pollRes.status === "ready" && isMounted) {
                setInsight(pollRes.data);
                setLoading(false);
                clearInterval(pollInterval);
              }
            } catch (pErr) {
              clearInterval(pollInterval);
            }
          }, 2500);
        } else if (fallbackContent && isMounted) {
          setInsight(fallbackContent);
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

  // Default content matching Stitch specifications if live insight is loading fallback
  const content = insight || fallbackContent || {
    technical_depth: "Intermediate Depth",
    estimated_read_time: 8,
    llm_model: "Claude 3.5 Sonnet",
    summary:
      "Introduces a hardware-aware routing mechanism for Mixture-of-Experts models that cuts memory bandwidth overhead by 42% on consumer GPUs without degrading ImageNet/MMLU benchmark accuracy. By restructuring routing tokens into static capacity-constrained clusters, the method avoids unpredictable buffer stalls during speculative decoding. Empirically validates sub-linear activation memory across 16-expert and 64-expert configurations.",
    key_takeaways: [
      "Replaces top-k token routing with static capacity-constrained expert blocks, yielding 1.8× faster inference.",
      "Open-source PyTorch & Triton kernels provided with verified FP8 support.",
      "Achieves 38 tokens/sec on a single RTX 4090 with 4-bit activation quantization.",
    ],
    why_it_matters:
      "Bridges the critical deployment gap between multi-hundred-billion parameter MoE architectures and edge or single-node workstation GPUs, making state-of-the-art reasoning models accessible without multi-node clusters.",
    related_topics: ["MoE", "TritonKernels", "EdgeInference"],
  };

  const depthLabel =
    content.technical_depth?.includes("Depth")
      ? content.technical_depth
      : `${content.technical_depth || "Intermediate"} Depth`;

  return (
    <div className="mt-4 pt-4 border-t border-dashed border-outline-variant/60 bg-surface -mx-5 -mb-5 p-5 rounded-b-xl">
      {/* Meta Bar */}
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
          <span>{content.llm_model ? `${content.llm_model} Synthesis` : "Claude 3.5 Sonnet Synthesis"}</span>
        </div>
      </div>

      {loading && !insight && !fallbackContent ? (
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
              {(content.related_topics || ["MoE", "TritonKernels", "EdgeInference"]).map(
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
