import React, { useState, useEffect } from "react";
import { TrendingUp, RefreshCw, Flame, BookOpen, ArrowRight, Sparkles } from "lucide-react";
import { api } from "../api/client";
import { DomainActivityLineChart } from "../components/trends/DomainActivityLineChart";
import { WeeklyComparisonBarChart } from "../components/trends/WeeklyComparisonBarChart";
import { TechRadarMatrix } from "../components/trends/TechRadarMatrix";
import { useFeedStore } from "../store/useFeedStore";

export function TrendsPage() {
  const setActiveRoute = useFeedStore((s) => s.setActiveRoute);
  const [window, setWindow] = useState("7d");
  const [trends, setTrends] = useState([]);
  const [allDomains, setAllDomains] = useState([]);
  const [topRisingDomains, setTopRisingDomains] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function load() {
      setLoading(true);
      try {
        const res = await api.getTrends(window);
        setTrends(res.trends || []);
        setAllDomains(res.all_domains || []);
        setTopRisingDomains(res.top_rising_domains || []);
      } catch (err) {
        console.error("Failed to load trends:", err);
      } finally {
        setLoading(false);
      }
    }
    load();
  }, [window]);

  // Aggregate current metrics per domain fallback
  const domainMap = {};
  trends.forEach((t) => {
    if (!domainMap[t.domain] || t.date > domainMap[t.domain].date) {
      domainMap[t.domain] = t;
    }
  });
  const latestDomains =
    allDomains.length > 0
      ? allDomains
      : Object.values(domainMap).sort(
          (a, b) => (b.wow_delta || 0) - (a.wow_delta || 0)
        );
  const topRising =
    topRisingDomains.length > 0
      ? topRisingDomains
      : latestDomains.slice(0, 3);

  return (
    <section className="flex-1 bg-surface-container-lowest px-8 py-6 min-h-screen">
      <div className="max-w-[960px] mx-auto space-y-8">
        {/* Page Header */}
        <div className="flex items-center justify-between flex-wrap gap-4 pb-4 border-b border-outline-variant/40">
          <div>
            <h2 className="font-headline-md text-headline-md font-semibold text-primary flex items-center gap-2">
              <TrendingUp className="w-5 h-5 text-[#10B981]" />
              <span>Trends &amp; Technology Radar</span>
            </h2>
            <p className="font-code-sm text-code-sm text-secondary mt-0.5">
              Macro-level velocity analytics, WoW comparison, and Hype vs. Adoption indicators
            </p>
          </div>

          {/* Controls: Time Window & Methodology Link */}
          <div className="flex items-center gap-3">
            <button
              onClick={() => setActiveRoute("/methodology")}
              className="inline-flex items-center gap-1.5 px-3 py-1 rounded-lg bg-surface border border-outline-variant/50 text-xs font-medium text-primary hover:bg-surface-container transition-colors"
            >
              <BookOpen className="w-3.5 h-3.5 text-[#10B981]" />
              <span>How Trends Are Judged</span>
              <ArrowRight className="w-3 h-3 text-secondary" />
            </button>

            <div className="inline-flex items-center p-0.5 bg-surface-container-low rounded-lg border border-outline-variant/40">
              <button
                onClick={() => setWindow("7d")}
                className={`px-3 py-1 rounded font-body-sm text-body-sm transition-colors ${
                  window === "7d"
                    ? "bg-surface-container-lowest text-on-surface font-medium border border-outline-variant/30 shadow-sm"
                    : "text-secondary hover:text-on-surface"
                }`}
              >
                7 Days Rolling
              </button>
              <button
                onClick={() => setWindow("30d")}
                className={`px-3 py-1 rounded font-body-sm text-body-sm transition-colors ${
                  window === "30d"
                    ? "bg-surface-container-lowest text-on-surface font-medium border border-outline-variant/30 shadow-sm"
                    : "text-secondary hover:text-on-surface"
                }`}
              >
                30 Days Rolling
              </button>
            </div>
          </div>
        </div>

        {loading ? (
          <div className="py-20 flex flex-col items-center justify-center text-secondary gap-3 bg-surface rounded-xl border border-outline-variant/40">
            <RefreshCw className="w-6 h-6 animate-spin text-[#10B981]" />
            <span className="font-code-sm text-code-sm">Aggregating historical velocity metrics...</span>
          </div>
        ) : (
          <>
            {/* Top 3 Rising Domains Summary Cards */}
            <div>
              <p className="font-label-caps text-label-caps uppercase tracking-wider text-outline font-semibold mb-3 flex items-center gap-1.5">
                <Flame className="w-4 h-4 text-[#F59E0B] fill-[#F59E0B]" />
                <span>Top Rising Technical Sectors (Steepest 7-Day Positive Slope)</span>
              </p>
              <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                {topRising.map((d, idx) => (
                  <div
                    key={d.domain}
                    className="bg-surface-container-lowest border border-outline-variant/50 rounded-xl p-4 shadow-sm"
                  >
                    <div className="flex items-center justify-between text-xs mb-2">
                      <span className="font-code-sm text-code-sm text-[#3730A3] bg-[#EEF2FF] px-2 py-0.5 rounded font-semibold border border-[#C7D2FE]">
                        #{idx + 1} Velocity Leader
                      </span>
                      <span className="text-[#10B981] font-bold font-code-sm text-code-sm">
                        +{Math.round((d.wow_delta || 0.1) * 100)}% WoW
                      </span>
                    </div>
                    <h3 className="font-headline-sm text-headline-sm font-semibold text-primary truncate mb-1">
                      {d.domain}
                    </h3>
                    <div className="flex items-center justify-between font-code-sm text-code-sm text-secondary mt-2 pt-2 border-t border-outline-variant/30">
                      <span>{d.item_count} items</span>
                      <span>Avg Impact: {d.avg_impact}/10</span>
                    </div>
                  </div>
                ))}
              </div>
            </div>

            {/* Recharts Analytics Charts */}
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
              <div className="bg-surface-container-lowest border border-outline-variant/50 rounded-xl p-5 shadow-sm">
                <DomainActivityLineChart trends={trends} />
              </div>
              <div className="bg-surface-container-lowest border border-outline-variant/50 rounded-xl p-5 shadow-sm">
                <WeeklyComparisonBarChart domains={latestDomains} />
              </div>
            </div>

            {/* 4-Quadrant Technology Radar Matrix */}
            <div className="bg-surface-container-lowest border border-outline-variant/50 rounded-xl p-5 shadow-sm">
              <TechRadarMatrix domains={latestDomains} />
            </div>
          </>
        )}
      </div>
    </section>
  );
}
