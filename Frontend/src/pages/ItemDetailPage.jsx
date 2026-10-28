import React, { useState, useEffect } from "react";
import { ArrowLeft, ExternalLink, Code2, BookOpen, Loader2 } from "lucide-react";
import { api } from "../api/client";
import { FullInsightCard } from "../components/detail/FullInsightCard";
import { PredictionWidget } from "../components/detail/PredictionWidget";
import { MetadataTable } from "../components/detail/MetadataTable";
import { DomainTag } from "../components/feed/DomainTag";
import { useFeedStore } from "../store/useFeedStore";

export function ItemDetailPage({ itemId }) {
  const setActiveRoute = useFeedStore((s) => s.setActiveRoute);
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function load() {
      if (!itemId) return;
      setLoading(true);
      try {
        const res = await api.getItem(itemId);
        setData(res);
      } catch (err) {
        console.error("Failed to load item:", err);
      } finally {
        setLoading(false);
      }
    }
    load();
  }, [itemId]);

  if (loading) {
    return (
      <section className="flex-1 bg-surface-container-lowest px-8 py-6 min-h-screen">
        <div className="max-w-[960px] mx-auto py-24 flex flex-col items-center justify-center text-secondary gap-3">
          <Loader2 className="w-6 h-6 animate-spin text-[#10B981]" />
          <span className="font-code-sm text-code-sm">Loading canonical intelligence deep-dive...</span>
        </div>
      </section>
    );
  }

  if (!data || !data.item) {
    return (
      <section className="flex-1 bg-surface-container-lowest px-8 py-6 min-h-screen">
        <div className="max-w-[960px] mx-auto bg-surface border border-outline-variant/40 p-12 text-center rounded-2xl my-6">
          <p className="font-headline-sm text-headline-sm text-primary mb-2">Item not found.</p>
          <button
            onClick={() => setActiveRoute("/")}
            className="px-4 py-2 rounded-lg bg-primary text-on-primary font-body-sm text-body-sm"
          >
            Return to Feed
          </button>
        </div>
      </section>
    );
  }

  const { item, classification, prediction, insight } = data;
  const meta = item.metadata || {};
  const hasCodeLink = meta.has_code || meta.github_repo_url;

  return (
    <section className="flex-1 bg-surface-container-lowest px-8 py-6 min-h-screen">
      <div className="max-w-[960px] mx-auto space-y-6">
        {/* Top Navigation & Action Header */}
        <div className="flex items-center justify-between gap-4 flex-wrap pb-4 border-b border-outline-variant/40">
          <button
            onClick={() => setActiveRoute("/")}
            className="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-lg bg-surface border border-outline-variant/40 text-on-surface hover:bg-surface-container text-xs font-medium transition-colors"
          >
            <ArrowLeft className="w-3.5 h-3.5" />
            <span>Back to Feed</span>
          </button>

          <div className="flex items-center gap-2">
            {item.source === "arxiv" && meta.pdf_url && (
              <a
                href={meta.pdf_url}
                target="_blank"
                rel="noopener noreferrer"
                className="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-lg bg-surface border border-outline-variant/40 hover:bg-surface-container text-on-surface text-xs font-medium transition-colors"
              >
                <BookOpen className="w-3.5 h-3.5" />
                <span>Download PDF</span>
                <ExternalLink className="w-3 h-3 opacity-60" />
              </a>
            )}
            <a
              href={item.url}
              target="_blank"
              rel="noopener noreferrer"
              className="inline-flex items-center gap-1.5 px-3.5 py-1.5 rounded-lg bg-primary text-on-primary text-xs font-medium hover:bg-surface-tint transition-colors"
            >
              <span>Open on {item.source.toUpperCase()}</span>
              <ExternalLink className="w-3.5 h-3.5" />
            </a>
          </div>
        </div>

        {/* Item Title & Hero Metadata */}
        <div>
          <div className="flex items-center gap-2 flex-wrap mb-2">
            {hasCodeLink && (
              <a
                href={meta.github_repo_url || item.url}
                target="_blank"
                rel="noopener noreferrer"
                className="inline-flex items-center gap-1.5 px-2.5 py-1 rounded bg-[#EEF2FF] text-[#3730A3] border border-[#C7D2FE] font-code-sm text-code-sm font-semibold"
              >
                <Code2 className="w-3.5 h-3.5" />
                <span>
                  Verified Code:{" "}
                  {meta.github_repo_url
                    ? meta.github_repo_url.replace("https://github.com/", "")
                    : "Linked"}
                </span>
                <ExternalLink className="w-2.5 h-2.5 opacity-60" />
              </a>
            )}
            {classification && (
              <DomainTag
                domain={classification.primary_domain}
                confidence={classification.confidence_scores?.[classification.primary_domain] || 0.85}
                isPrimary={true}
              />
            )}
          </div>

          <h1 className="font-headline-lg text-headline-lg font-semibold text-primary leading-snug mb-2">
            {item.title}
          </h1>

          {meta.authors && meta.authors.length > 0 && (
            <p className="font-code-sm text-code-sm text-secondary">
              Authors: <span className="text-on-surface">{meta.authors.join(", ")}</span>
            </p>
          )}
        </div>

        {/* 2-Column Asymmetric Deep Dive Layout */}
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
          {/* Left Column (60% width): Evidence & Synthesis */}
          <div className="lg:col-span-7 space-y-6">
            <div className="bg-surface-container-lowest border border-outline-variant/50 rounded-xl p-5 shadow-sm">
              <FullInsightCard item={item} insight={insight} />
            </div>
            <div className="bg-surface-container-lowest border border-outline-variant/50 rounded-xl p-5 shadow-sm">
              <MetadataTable item={item} />
            </div>
          </div>

          {/* Right Column (40% width): ML Prediction Engine */}
          <div className="lg:col-span-5 space-y-6">
            <div className="bg-surface-container-lowest border border-outline-variant/50 rounded-xl p-5 shadow-sm">
              <PredictionWidget prediction={prediction} source={item.source} />
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}
