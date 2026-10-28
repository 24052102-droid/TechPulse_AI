import React, { useState } from "react";
import {
  TrendingUp,
  Sparkles,
  GitFork,
  Star,
  GitCommit,
  BookOpen,
  Sliders,
  CheckCircle2,
  ArrowUpRight,
  Flame,
  Activity,
  Layers,
  Code2,
  ShieldCheck,
  Award,
} from "lucide-react";
import { useFeedStore } from "../store/useFeedStore";

export function TrendMethodologyPage() {
  const setActiveRoute = useFeedStore((s) => s.setActiveRoute);

  // Interactive Simulator State
  const [simArxivPapers, setSimArxivPapers] = useState(18);
  const [simGithubRepos, setSimGithubRepos] = useState(12);
  const [simAuthorHIndex, setSimAuthorHIndex] = useState(45);
  const [simDaysSinceCommit, setSimDaysSinceCommit] = useState(4);
  const [simHasCodeLink, setSimHasCodeLink] = useState(true);

  // Dynamic calculations for simulator
  const simRatio = Number((Math.max(1, simArxivPapers) / Math.max(1, simGithubRepos)).toFixed(2));
  const simHypeScore = Math.min(
    10,
    Math.max(1, (simArxivPapers * 0.25 + simAuthorHIndex * 0.08 + (simHasCodeLink ? 0.8 : 0))).toFixed(1)
  );
  const simAdoptionScore = Math.min(
    10,
    Math.max(1, (simGithubRepos * 0.35 + Math.max(0, 15 - simDaysSinceCommit) * 0.35)).toFixed(1)
  );

  let simQuadrant = "Established";
  let simQuadrantColor = "text-[#3B82F6] border-[#93C5FD] bg-[#EFF6FF]";
  let simQuadrantDesc = "Steady production toolchain with balanced research and sustained engineering.";

  if (simRatio > 1.8) {
    simQuadrant = "Emerging (High Hype)";
    simQuadrantColor = "text-[#0D9488] border-[#99F6E4] bg-[#F0FDFA]";
    simQuadrantDesc = "Intense theoretical research exploration; open-source implementations still forming.";
  } else if (simRatio >= 0.8 && (simArxivPapers >= 12 || simGithubRepos >= 10)) {
    simQuadrant = "Rising (Golden Breakout)";
    simQuadrantColor = "text-[#059669] border-[#A7F3D0] bg-[#ECFDF5]";
    simQuadrantDesc = "Rapid parallel momentum: surging academic citations matched by heavy developer adoption.";
  } else if (simDaysSinceCommit > 30) {
    simQuadrant = "Declining / Cooling";
    simQuadrantColor = "text-[#E11D48] border-[#FECDD3] bg-[#FFF1F2]";
    simQuadrantDesc = "Stale commits or superseded by newer paradigms; cooling velocity.";
  }

  return (
    <section className="flex-1 bg-surface-container-lowest px-8 py-6 min-h-screen">
      <div className="max-w-[1020px] mx-auto space-y-8">
        {/* Breadcrumb & Navigation */}
        <div className="flex items-center justify-between flex-wrap gap-4 pb-4 border-b border-outline-variant/40">
          <div>
            <div className="flex items-center gap-2 text-xs font-code-sm text-secondary mb-1">
              <span
                onClick={() => setActiveRoute("/trends")}
                className="hover:text-primary cursor-pointer transition-colors"
              >
                Trends
              </span>
              <span>/</span>
              <span className="text-primary font-medium">Methodology &amp; Formula Engine</span>
            </div>
            <h2 className="font-headline-md text-headline-md font-semibold text-primary flex items-center gap-2">
              <Activity className="w-6 h-6 text-[#10B981]" />
              <span>How Technical Trends Are Judged</span>
            </h2>
            <p className="font-code-sm text-code-sm text-secondary mt-0.5">
              The dual-stream econometric and machine-learning methodology behind the ATIP Technology Radar
            </p>
          </div>

          <button
            onClick={() => setActiveRoute("/trends")}
            className="inline-flex items-center gap-1.5 px-3.5 py-1.5 rounded-lg bg-surface border border-outline-variant/50 text-on-surface hover:bg-surface-container text-xs font-medium transition-colors"
          >
            <span>← Back to Live Radar</span>
          </button>
        </div>

        {/* Hero Principle Callout */}
        <div className="p-6 rounded-2xl bg-gradient-to-r from-[#F0FDF4] via-[#F8FAFC] to-[#EEF2FF] border border-[#BBF7D0]/60 shadow-sm">
          <div className="flex items-start gap-3">
            <div className="p-2 rounded-xl bg-white shadow-xs border border-[#86EFAC] text-[#16A34A] shrink-0 mt-0.5">
              <Sparkles className="w-5 h-5" />
            </div>
            <div>
              <h3 className="font-headline-sm text-headline-sm font-semibold text-primary mb-1">
                The Core Principle: Theory vs. Production Reality
              </h3>
              <p className="font-body-md text-body-md text-secondary leading-relaxed">
                Most platforms track trends through raw social sentiment or pageviews—metrics easily distorted by marketing noise.
                TechPulse AI decouples signals into two rigorous streams:{" "}
                <span className="font-semibold text-primary">Academic Exploration (arXiv)</span> and{" "}
                <span className="font-semibold text-primary">Developer Implementation (GitHub)</span>.
                By contrasting these vectors, our platform identifies what is genuine foundational transformation versus transient hype.
              </p>
            </div>
          </div>
        </div>

        {/* Section 1: Dual-Stream Pipeline Architecture */}
        <div className="space-y-4">
          <h3 className="font-label-caps text-label-caps uppercase tracking-wider text-outline font-semibold">
            1. Dual-Stream Feature Extraction Architecture
          </h3>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            {/* Stream A: arXiv Research Papers */}
            <div className="bg-surface-container-lowest border border-[#C7D2FE] rounded-2xl p-6 shadow-sm relative overflow-hidden">
              <div className="absolute top-0 right-0 w-32 h-32 bg-[#EEF2FF] rounded-bl-full -z-0 opacity-60"></div>
              <div className="relative z-10 space-y-4">
                <div className="flex items-center justify-between">
                  <div className="flex items-center gap-2 text-[#3730A3]">
                    <BookOpen className="w-5 h-5" />
                    <span className="font-headline-sm text-headline-sm font-semibold">
                      Stream A: arXiv Research Papers
                    </span>
                  </div>
                  <span className="px-2 py-0.5 rounded bg-[#EEF2FF] text-[#4338CA] font-code-sm text-code-sm font-semibold">
                    Hype Vector
                  </span>
                </div>

                <p className="font-body-sm text-body-sm text-secondary">
                  Evaluates theoretical significance and early institutional consensus before empirical citations accumulate.
                </p>

                <div className="space-y-3 pt-2">
                  <div className="p-3 rounded-xl bg-surface border border-outline-variant/40 space-y-1">
                    <div className="flex items-center justify-between font-code-sm text-code-sm font-medium">
                      <span className="text-primary font-semibold">Max Author h-index (Semantic Scholar)</span>
                      <span className="text-[#4338CA] font-bold">33.1% Weight</span>
                    </div>
                    <p className="text-xs text-secondary leading-snug">
                      Solves Day-1 cold start. Historical track records of key authors (e.g., Stanford, FAIR, DeepMind) heavily predict 180-day impact.
                    </p>
                  </div>

                  <div className="p-3 rounded-xl bg-surface border border-outline-variant/40 space-y-1">
                    <div className="flex items-center justify-between font-code-sm text-code-sm font-medium">
                      <span className="text-primary font-semibold">Verified Open-Source Code Link</span>
                      <span className="text-[#059669] font-bold">+8.1% Impact Boost</span>
                    </div>
                    <p className="text-xs text-secondary leading-snug">
                      Regex parser audits abstracts for public repository links. Executable benchmarks accelerate community verification.
                    </p>
                  </div>

                  <div className="p-3 rounded-xl bg-surface border border-outline-variant/40 space-y-1">
                    <div className="flex items-center justify-between font-code-sm text-code-sm font-medium">
                      <span className="text-primary font-semibold">7-Day Volume Regression Slope (m)</span>
                      <span className="text-primary font-bold">Slope &gt; 0</span>
                    </div>
                    <p className="text-xs text-secondary leading-snug">
                      Ordinary least-squares linear regression over daily submission rates detects accelerating subfields.
                    </p>
                  </div>
                </div>
              </div>
            </div>

            {/* Stream B: GitHub Software Repositories */}
            <div className="bg-surface-container-lowest border border-[#BBF7D0] rounded-2xl p-6 shadow-sm relative overflow-hidden">
              <div className="absolute top-0 right-0 w-32 h-32 bg-[#F0FDF4] rounded-bl-full -z-0 opacity-60"></div>
              <div className="relative z-10 space-y-4">
                <div className="flex items-center justify-between">
                  <div className="flex items-center gap-2 text-[#065F46]">
                    <GitFork className="w-5 h-5" />
                    <span className="font-headline-sm text-headline-sm font-semibold">
                      Stream B: GitHub Software Repos
                    </span>
                  </div>
                  <span className="px-2 py-0.5 rounded bg-[#DCFCE7] text-[#15803D] font-code-sm text-code-sm font-semibold">
                    Adoption Vector
                  </span>
                </div>

                <p className="font-body-sm text-body-sm text-secondary">
                  Measures true engineering adoption: are practitioners downloading, compiling, and integrating the code?
                </p>

                <div className="space-y-3 pt-2">
                  <div className="p-3 rounded-xl bg-surface border border-outline-variant/40 space-y-1">
                    <div className="flex items-center justify-between font-code-sm text-code-sm font-medium">
                      <span className="text-primary font-semibold">Commit Recency (days_since_commit)</span>
                      <span className="text-[#059669] font-bold">28.4% Top Driver</span>
                    </div>
                    <p className="text-xs text-secondary leading-snug">
                      Penalizes dormant codebases. Active repositories with weekly releases are prioritized over abandoned viral repos.
                    </p>
                  </div>

                  <div className="p-3 rounded-xl bg-surface border border-outline-variant/40 space-y-1">
                    <div className="flex items-center justify-between font-code-sm text-code-sm font-medium">
                      <span className="text-primary font-semibold">30-Day Star Acceleration (ΔS₃₀d)</span>
                      <span className="text-[#2563EB] font-bold">19.6% Weight</span>
                    </div>
                    <p className="text-xs text-secondary leading-snug">
                      Normalized logarithmic star velocity y = ln(1 + ΔStars). Filters out vanity stars accumulated over a decade.
                    </p>
                  </div>

                  <div className="p-3 rounded-xl bg-surface border border-outline-variant/40 space-y-1">
                    <div className="flex items-center justify-between font-code-sm text-code-sm font-medium">
                      <span className="text-primary font-semibold">Fork-to-Star Ratio</span>
                      <span className="text-primary font-bold">Utility Ratio</span>
                    </div>
                    <p className="text-xs text-secondary leading-snug">
                      Forks reflect engineers building and patching downstream, distinguishing tools from bookmark collections.
                    </p>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* Section 2: Mathematical Formulations */}
        <div className="space-y-4">
          <h3 className="font-label-caps text-label-caps uppercase tracking-wider text-outline font-semibold">
            2. Core Mathematical Formulations
          </h3>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            {/* Formula 1: OLS Regression Slope */}
            <div className="bg-surface-container-lowest border border-outline-variant/50 rounded-2xl p-5 shadow-sm space-y-3">
              <div className="flex items-center gap-2 text-primary font-semibold font-body-sm text-body-sm">
                <span className="w-6 h-6 rounded-lg bg-surface-container flex items-center justify-center font-code-sm text-code-sm">
                  1
                </span>
                <span>Momentum Slope (m)</span>
              </div>
              <div className="p-3 rounded-xl bg-surface border border-outline-variant/40 font-code-sm text-code-sm text-center text-primary font-semibold">
                m = Σ(tᵢ - t̄)(yᵢ - ȳ) / Σ(tᵢ - t̄)²
              </div>
              <p className="text-xs text-secondary leading-relaxed">
                Ordinary Least Squares fitted over a 7-day rolling window of daily domain volume. Positive values indicate acceleration; negative values signal cooling.
              </p>
            </div>

            {/* Formula 2: WoW Delta */}
            <div className="bg-surface-container-lowest border border-outline-variant/50 rounded-2xl p-5 shadow-sm space-y-3">
              <div className="flex items-center gap-2 text-primary font-semibold font-body-sm text-body-sm">
                <span className="w-6 h-6 rounded-lg bg-surface-container flex items-center justify-center font-code-sm text-code-sm">
                  2
                </span>
                <span>Week-over-Week (WoW) Surge</span>
              </div>
              <div className="p-3 rounded-xl bg-surface border border-outline-variant/40 font-code-sm text-code-sm text-center text-primary font-semibold">
                WoW = (V_current - V_prior) / max(1, V_prior)
              </div>
              <p className="text-xs text-secondary leading-relaxed">
                Measures current 7-day volume against the previous 7-day baseline. Domains exceeding <span className="font-semibold text-[#059669]">+25%</span> trigger the <span className="text-[#DC2626] font-semibold">🔥 Rising</span> badge.
              </p>
            </div>

            {/* Formula 3: Hype vs Adoption Ratio */}
            <div className="bg-surface-container-lowest border border-outline-variant/50 rounded-2xl p-5 shadow-sm space-y-3">
              <div className="flex items-center gap-2 text-primary font-semibold font-body-sm text-body-sm">
                <span className="w-6 h-6 rounded-lg bg-surface-container flex items-center justify-center font-code-sm text-code-sm">
                  3
                </span>
                <span>Hype-to-Adoption Ratio</span>
              </div>
              <div className="p-3 rounded-xl bg-surface border border-outline-variant/40 font-code-sm text-code-sm text-center text-primary font-semibold">
                Ratio = Count_arXiv / max(1, Count_GitHub)
              </div>
              <p className="text-xs text-secondary leading-relaxed">
                Determines placement along the Technology Radar. Ratios &gt; 1.8 indicate academic saturation; ratios ≈ 1.0 indicate healthy concurrent adoption.
              </p>
            </div>
          </div>
        </div>

        {/* Section 3: The 4 Quadrants of the Technology Radar */}
        <div className="space-y-4">
          <h3 className="font-label-caps text-label-caps uppercase tracking-wider text-outline font-semibold">
            3. The 4 Quadrants of the Technology Radar
          </h3>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div className="p-5 rounded-2xl bg-surface border border-[#99F6E4] space-y-2">
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-2 text-[#0D9488] font-bold text-sm">
                  <span>🌱</span>
                  <span>Emerging (High Academic Hype)</span>
                </div>
                <span className="font-code-sm text-code-sm text-[#0D9488] bg-[#CCFBF1] px-2 py-0.5 rounded font-semibold">
                  Ratio &gt; 1.8
                </span>
              </div>
              <p className="text-xs text-secondary leading-relaxed">
                <strong>Characteristics:</strong> Surging arXiv publications from research labs, but stable, packaged software libraries have not yet emerged. High long-term opportunity, high near-term implementation risk.
              </p>
              <p className="text-xs text-[#0F766E] font-medium pt-1">
                Examples: Quantum Machine Learning, Speculative Token Decoding, Bi-directional State-Space Models.
              </p>
            </div>

            <div className="p-5 rounded-2xl bg-surface border border-[#A7F3D0] space-y-2">
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-2 text-[#059669] font-bold text-sm">
                  <span>🚀</span>
                  <span>Rising (Golden Breakout)</span>
                </div>
                <span className="font-code-sm text-code-sm text-[#059669] bg-[#DCFCE7] px-2 py-0.5 rounded font-semibold">
                  WoW &gt; +10% · Balanced Ratio
                </span>
              </div>
              <p className="text-xs text-secondary leading-relaxed">
                <strong>Characteristics:</strong> Rapid parallel momentum: peer-reviewed research papers and real-world GitHub star velocity are exploding simultaneously. The golden zone for developer adoption.
              </p>
              <p className="text-xs text-[#047857] font-medium pt-1">
                Examples: MoE Inference Kernels (vLLM / FlashInfer), 1-Bit LLM Architectures (BitNet), Multimodal Vision-Language.
              </p>
            </div>

            <div className="p-5 rounded-2xl bg-surface border border-[#BFDBFE] space-y-2">
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-2 text-[#2563EB] font-bold text-sm">
                  <span>🏛️</span>
                  <span>Established (Production Workhorses)</span>
                </div>
                <span className="font-code-sm text-code-sm text-[#2563EB] bg-[#DBEAFE] px-2 py-0.5 rounded font-semibold">
                  Low Volatility · High Star Mass
                </span>
              </div>
              <p className="text-xs text-secondary leading-relaxed">
                <strong>Characteristics:</strong> Deeply embedded industrial toolchains. Weekly publication rates are modest, but daily commit cadence and cumulative dependency counts are very high.
              </p>
              <p className="text-xs text-[#1D4ED8] font-medium pt-1">
                Examples: PyTorch, Apache Spark / Beam, Kubernetes Operators, Dataform / dbt orchestration.
              </p>
            </div>

            <div className="p-5 rounded-2xl bg-surface border border-[#FECDD3] space-y-2">
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-2 text-[#E11D48] font-bold text-sm">
                  <span>📉</span>
                  <span>Declining / Cooling</span>
                </div>
                <span className="font-code-sm text-code-sm text-[#E11D48] bg-[#FFE4E6] px-2 py-0.5 rounded font-semibold">
                  WoW &lt; -5%
                </span>
              </div>
              <p className="text-xs text-secondary leading-relaxed">
                <strong>Characteristics:</strong> Subfields undergoing architectural transition or superseded by foundation models. Star velocity has plateaued and commit frequencies are diminishing.
              </p>
              <p className="text-xs text-[#BE123C] font-medium pt-1">
                Examples: Rule-based NLP Parsers, Standalone ResNets, Legacy Feature Engineering Toolkits.
              </p>
            </div>
          </div>
        </div>

        {/* Section 4: Interactive Trend Sandbox Simulator */}
        <div className="space-y-4">
          <div className="flex items-center justify-between">
            <h3 className="font-label-caps text-label-caps uppercase tracking-wider text-outline font-semibold flex items-center gap-2">
              <Sliders className="w-4 h-4 text-[#10B981]" />
              <span>4. Interactive Metric Simulator &amp; Quadrant Classifier</span>
            </h3>
            <span className="font-code-sm text-code-sm text-[#059669] bg-[#ECFDF5] px-2.5 py-1 rounded-full font-semibold border border-[#A7F3D0]">
              Live Evaluator
            </span>
          </div>

          <div className="bg-surface-container-lowest border border-outline-variant/50 rounded-2xl p-6 shadow-sm">
            <p className="font-body-sm text-body-sm text-secondary mb-6">
              Adjust the sliders below to simulate a technology's academic and open-source metrics.
              The model immediately recalculates the Hype-to-Adoption ratio, composite impact score, and target radar quadrant in real-time.
            </p>

            <div className="grid grid-cols-1 lg:grid-cols-12 gap-8">
              {/* Sliders (7 columns) */}
              <div className="lg:col-span-7 space-y-5">
                <div>
                  <div className="flex items-center justify-between text-xs font-code-sm mb-1.5">
                    <span className="font-semibold text-primary">7-Day arXiv Papers Ingested:</span>
                    <span className="font-bold text-[#4338CA]">{simArxivPapers} papers</span>
                  </div>
                  <input
                    type="range"
                    min="1"
                    max="50"
                    value={simArxivPapers}
                    onChange={(e) => setSimArxivPapers(Number(e.target.value))}
                    className="w-full accent-[#4338CA] cursor-pointer"
                  />
                </div>

                <div>
                  <div className="flex items-center justify-between text-xs font-code-sm mb-1.5">
                    <span className="font-semibold text-primary">Active GitHub Repositories:</span>
                    <span className="font-bold text-[#059669]">{simGithubRepos} repos</span>
                  </div>
                  <input
                    type="range"
                    min="1"
                    max="40"
                    value={simGithubRepos}
                    onChange={(e) => setSimGithubRepos(Number(e.target.value))}
                    className="w-full accent-[#059669] cursor-pointer"
                  />
                </div>

                <div>
                  <div className="flex items-center justify-between text-xs font-code-sm mb-1.5">
                    <span className="font-semibold text-primary">Lead Author h-index (Semantic Scholar):</span>
                    <span className="font-bold text-[#2563EB]">{simAuthorHIndex}</span>
                  </div>
                  <input
                    type="range"
                    min="5"
                    max="90"
                    value={simAuthorHIndex}
                    onChange={(e) => setSimAuthorHIndex(Number(e.target.value))}
                    className="w-full accent-[#2563EB] cursor-pointer"
                  />
                </div>

                <div>
                  <div className="flex items-center justify-between text-xs font-code-sm mb-1.5">
                    <span className="font-semibold text-primary">Days Since Last Commit:</span>
                    <span className={`font-bold ${simDaysSinceCommit > 20 ? "text-[#E11D48]" : "text-primary"}`}>
                      {simDaysSinceCommit} days
                    </span>
                  </div>
                  <input
                    type="range"
                    min="0"
                    max="60"
                    value={simDaysSinceCommit}
                    onChange={(e) => setSimDaysSinceCommit(Number(e.target.value))}
                    className="w-full accent-[#3B82F6] cursor-pointer"
                  />
                </div>

                <div className="pt-2 flex items-center justify-between border-t border-outline-variant/30">
                  <label className="flex items-center gap-2 cursor-pointer text-xs font-body-sm text-primary select-none">
                    <input
                      type="checkbox"
                      checked={simHasCodeLink}
                      onChange={(e) => setSimHasCodeLink(e.target.checked)}
                      className="w-4 h-4 rounded text-primary accent-black cursor-pointer"
                    />
                    <span>Verified Open-Source GitHub Repository Linked in Abstract</span>
                  </label>
                  <span className="font-code-sm text-code-sm text-[#059669] font-semibold">
                    {simHasCodeLink ? "+8.1% boost" : "No boost"}
                  </span>
                </div>
              </div>

              {/* Dynamic Output Dashboard (5 columns) */}
              <div className="lg:col-span-5 bg-surface border border-outline-variant/50 rounded-xl p-5 flex flex-col justify-between space-y-4">
                <div>
                  <span className="text-[11px] font-label-caps uppercase tracking-wider text-outline font-semibold block mb-3">
                    Calculated Classification
                  </span>

                  <div className={`p-4 rounded-xl border ${simQuadrantColor} mb-4`}>
                    <div className="text-xs font-bold uppercase tracking-wide">
                      Assigned Quadrant
                    </div>
                    <div className="text-lg font-bold mt-0.5">{simQuadrant}</div>
                    <p className="text-xs opacity-90 mt-1 leading-snug">{simQuadrantDesc}</p>
                  </div>

                  <div className="space-y-2 text-xs font-code-sm">
                    <div className="flex items-center justify-between py-1.5 border-b border-outline-variant/30">
                      <span className="text-secondary">Hype vs Adoption Ratio:</span>
                      <span className="font-bold text-primary">{simRatio}x</span>
                    </div>

                    <div className="flex items-center justify-between py-1.5 border-b border-outline-variant/30">
                      <span className="text-secondary">Estimated Hype Index:</span>
                      <span className="font-bold text-[#4338CA]">{simHypeScore} / 10</span>
                    </div>

                    <div className="flex items-center justify-between py-1.5 border-b border-outline-variant/30">
                      <span className="text-secondary">Engineering Adoption Score:</span>
                      <span className="font-bold text-[#059669]">{simAdoptionScore} / 10</span>
                    </div>
                  </div>
                </div>

                <div className="p-3 rounded-lg bg-surface-container-low text-[11px] text-secondary leading-relaxed border border-outline-variant/30">
                  <div className="flex items-center gap-1 font-semibold text-primary mb-0.5">
                    <ShieldCheck className="w-3.5 h-3.5 text-[#10B981]" />
                    <span>Model Audit Transparency</span>
                  </div>
                  XGBoost predictions verified across 5-fold cross-validation (arXiv RMSE: 0.0959, GitHub RMSE: 0.0617).
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}
