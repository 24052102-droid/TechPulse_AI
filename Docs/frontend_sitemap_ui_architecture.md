# ATIP (TechPulse AI) — Frontend Sitemap & Minimal UI Specification

**Project:** Autonomous Technical Intelligence & Prediction Platform (ATIP / TechPulse AI)  
**Stack:** React 18 · Vite · TailwindCSS · Recharts · Zustand · TanStack Query · Lucide Icons  
**Design Paradigm:** Minimalist, Signal-First, Progressive Disclosure (Linear / Vercel / Semantic Scholar aesthetic)

---

## 1. Minimalist UI & Navigation Philosophy

To prevent the platform from recreating the very "information overload" it is trying to solve, the frontend merges the routes from the **ATIP TRD** and the **TechPulse AI Brief** into a **3-Pillar Navigation Architecture** plus one **Detail View** and one **Global Slide-Over Assistant**:

1. **Progressive Disclosure (Zero Clutter):** Item cards in the main feed display only 4 core signals by default (Title, Source/Code Link, Domain Tag, Explainable Impact Score). Deep LLM synthesis is hidden inside a lazy-loaded, single-click expandable panel (`InsightPanel`).
2. **Consolidated Filtering (No Page Jumps):** Instead of forcing users to bounce between `/`, `/explore/:domain`, and `/search`, all discovery happens inside a single unified **Intelligence Feed** view using URL-synced Zustand state (`/?domains=nlp,cv&q=diffusion&sort=impact`).
3. **Explainable AI by Default:** Per the project brief, no raw score is shown as "magic." Hovering over any Impact Score or Classification Tag reveals the exact model confidence, top 3 contributing features, and prediction horizon.
4. **No Auth Friction:** Zero login walls, popups, or onboarding modals. The app loads directly into the live intelligence feed in $< 2\text{s}$.

---

## 2. High-Level Information Architecture (Sitemap Tree)

```text
ATIP Web Application (Root Layout Shell)
│
├── Persistent Left Sidebar (Navigation + 10-Domain Multi-Select Filter)
├── Persistent Top Command Bar (Natural Language Search + Pipeline Status Pill + AI Drawer Toggle)
├── Global Slide-Over Drawer: Evidence-Grounded RAG Assistant (Accessible from any route via Cmd+K / Button)
│
├── 1. [ / ] Intelligence Feed (Main Dashboard)
│   ├── [ /explore/:domain ] ──▶ Pre-filtered state of Main Feed + Domain Header Banner
│   ├── [ /search?q=... ]    ──▶ Ranked Search State (Text Relevance × 0.4 + Impact Score × 0.6)
│   └── Inline Expandable: <InsightPanel /> (Lazy-loaded LLM summary, takeaways, depth, read time)
│
├── 2. [ /trends ] Trends & Technology Radar
│   ├── Section A: Domain Velocity (7d / 30d Line Chart & WoW Comparison Bar Chart)
│   ├── Section B: Technology Radar Matrix (Emerging · Rising · Established · Declining)
│   └── Section C: Hype vs. Adoption Signals & Candidate Research Opportunities
│
├── 3. [ /item/:id ] Item Deep-Dive View (Paper / Repo / HN Article)
│   ├── Header: Canonical Metadata + Paper-to-Repository Link Badge
│   ├── Left Column: Full Grounded LLM Analysis (Claims, Methodology, Limitations, Research Gaps)
│   └── Right Column: Explainable ML Prediction Widget (Score Gauge, 30d/180d Growth Forecast, Feature Drivers)
│
└── 4. [ /evaluation ] System Health & Model Evaluation (Faculty Review / "Killer Demo" View)
    ├── Live Pipeline Telemetry (Last Ingestion Cron, DB/Redis Ping, Manual Refresh Trigger)
    ├── Domain Classifier Benchmarks (Top-1 Accuracy ≥ 85%, Macro F1 ≥ 0.80, Per-Domain Breakdown)
    └── Impact Predictor Backtesting (RMSE ≤ 0.20, Prediction vs. Reality Historical Scatter)
```

---

## 3. Global App Shell & Visual Layout

### 3.1 Color, Typography & Density Tokens
* **Backgrounds:** Pure Alabaster (`#FAFAFA`) in Light Mode / Obsidian Slate (`#090D16`) in Dark Mode. Cards use subtle `1px` borders (`border-slate-200` / `border-slate-800`) instead of heavy drop shadows.
* **Typography:**
  * *UI & Body:* `Inter` or `Geist Sans` (clean, legible at `14px`).
  * *Metrics, Scores & IDs:* `JetBrains Mono` (tabular numerals for impact scores, arXiv IDs, star counts, and confidence percentages).
* **Semantic Signal Accents:**
  * **High Impact ($7.5 - 10.0$):** Emerald (`#10B981`)
  * **Moderate Impact ($4.0 - 7.4$):** Amber (`#F59E0B`)
  * **Low / Baseline ($0.0 - 3.9$):** Slate/Rose (`#64748B` / `#F43F5E`)
  * **Source Badges:** arXiv (Crimson Red tint), GitHub (Neutral Dark tint), Hacker News (Orange tint).

### 3.2 Persistent Application Wireframe (Desktop `1440px`)

```text
+--------------------------------------------------------------------------------------------------+
| [ATIP Logo]   [ 🔍 Search papers, repos, or concepts... (Cmd+K)     ]  [● Pipeline: 2h ago] [✨ Ask AI] |
+----------------------+---------------------------------------------------------------------------+
| PRIMARY NAV          |                                                                           |
| ● Intelligence Feed  |                                                                           |
| ○ Trends & Radar     |                                                                           |
| ○ Model Evaluation   |                                                                           |
|                      |                        MAIN VIEWPORT AREA                                 |
| -------------------- |                   (Max-width: 960px centered)                             |
| SOURCE TYPE          |                                                                           |
| [All] [arXiv] [Git]  |      Renders active route:                                                |
|                      |      1. / (Intelligence Feed)                                             |
| DOMAINS (Multi) [Reset]     2. /trends (Trends & Technology Radar)                               |
| [x] NLP         (142)|      3. /item/:id (Item Deep-Dive)                                        |
| [x] Comp Vision  (98)|      4. /evaluation (Faculty Review & Telemetry)                          |
| [ ] Multimodal   (64)|                                                                           |
| [ ] Systems/Infra(51)|                                                                           |
| [ ] Reinforce. L (29)|                                                                           |
| [ ] Robotics     (19)|                                                                           |
| [ ] Security     (24)|                                                                           |
| [ ] IoT/Embedded (15)|                                                                           |
| [ ] Data Eng     (31)|                                                                           |
| [ ] General ML   (88)|                                                                           |
+----------------------+---------------------------------------------------------------------------+
```

* **Mobile / Tablet Responsiveness (`< 768px`):** The left sidebar collapses into a bottom navigation bar (`Feed`, `Filter Drawer`, `Trends`, `Eval`), and the search bar condenses into an expandable top icon.

---

## 4. Detailed Page-by-Page Breakdown & Wireframes

### Page 1: Intelligence Feed (`/`, `/explore/:domain`, `/search`)
**Purpose:** Primary workspace for Persona 1 (ML Researcher) and Persona 2 (Open-Source Developer) to triage daily technical output in under 5 minutes.

#### Visual Layout & Components:
1. **Trending Pulse Strip (`<TrendingBanner />`):** A minimal single-line ticker at the top highlighting the top 3 spiking items over the last 48 hours.
2. **Feed Control Bar:** Displays active filter chips (e.g., `NLP ×`, `Computer Vision ×`) on the left, and a compact Sort Selector (`Impact Score ↓` | `Recent` | `48h Velocity`) on the right.
3. **Feed Card List (`<FeedList />` & `<ItemCard />`):** Paginated at 20 items/page with sub-2s load time.

#### `<ItemCard />` + Expandable `<InsightPanel />` Wireframe:
```text
+--------------------------------------------------------------------------------------------------+
| [arXiv:2610.14201]  [🔗 Code Linked: github.com/org/repo]                      Ingested 3h ago   |
|                                                                                                  |
| Sparse-MoE Scaling Laws for Edge-Deployed Vision Transformers                                    |
|                                                                                                  |
| [NLP · 91%] [IoT/Embedded · 24%]     [🔥 Rising]     Impact: 8.7/10 [████████░░] (ⓘ Top drivers) |
|                                                                                                  |
| [ ▾ Expand AI Insights (12 min read · Intermediate) ]                       [Full Deep-Dive ↗]   |
| - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -  |
| (Expanded State — Lazy-loaded via GET /api/item/{id}/insights with skeleton fallback)            |
|                                                                                                  |
| SUMMARY                                                                                          |
| Introduces a hardware-aware routing mechanism for Mixture-of-Experts vision models that cuts     |
| memory bandwidth by 42% on ARM NPUs without degrading ImageNet top-1 accuracy...                 |
|                                                                                                  |
| KEY TECHNICAL TAKEAWAYS                                                                          |
| • Replaces top-k token routing with static capacity-constrained expert blocks.                   |
| • Achieves 38 FPS on Raspberry Pi 5 with 4-bit activation quantization.                          |
| • Includes open-source PyTorch & ONNX export kernels (verified repo match).                      |
|                                                                                                  |
| WHY IT MATTERS                                                                                   |
| Bridges the gap between foundation-scale vision models and constrained embedded IoT hardware...  |
|                                                                                                  |
| Related: [#edge-inference] [#mixture-of-experts] [#quantization]                                 |
+--------------------------------------------------------------------------------------------------+
```
* **Hover Micro-Interactions:**
  * Hovering over `[NLP · 91%]` shows tooltip: `Model: BART-large-MNLI | Confidence: 0.91`.
  * Hovering over `Impact: 8.7/10` shows tooltip: `Predicted 6-mo Citations: Top Decile | Top Drivers: 1. Max Author h-index (42), 2. Verified GitHub Link, 3. Abstract Readability`.

---

### Page 2: Trends & Technology Radar (`/trends`)
**Purpose:** Macro-level intelligence combining ATIP's Recharts analytics with TechPulse AI's Technology Radar and Hype vs. Adoption indicators.

#### Visual Layout:
```text
+--------------------------------------------------------------------------------------------------+
| TRENDS & TECHNOLOGY RADAR                                      Window: [ 7 Days ] [ 30 Days ]    |
+--------------------------------------------------------------------------------------------------+
| TOP RISING DOMAINS (Steepest 7-Day Positive Slope)                                               |
| +-------------------------------+ +-------------------------------+ +--------------------------+ |
| | 1. Multimodal AI     +34% WoW | | 2. IoT & Embedded    +26% WoW | | 3. Robotics     +21% WoW | |
| | Avg Impact: 7.4 · 64 items    | | Avg Impact: 6.9 · 15 items    | | Avg Impact: 7.1 · 19 itm | |
| +-------------------------------+ +-------------------------------+ +--------------------------+ |
|                                                                                                  |
| +-----------------------------------------------+ +--------------------------------------------+ |
| | DOMAIN ACTIVITY OVER TIME (Recharts Line)     | | THIS WEEK VS. LAST WEEK (Recharts Bar)     | |
| |   ^                                           | |   NLP      ████████████ 142 (vs 128)       | |
| |   |      /\_/\  Multimodal                    | |   CV       █████████ 98 (vs 104)           | |
| |   |  ___/     \___ NLP                        | |   Systems  ██████ 51 (vs 39)               | |
| |   +--------------------------------------->   | |   IoT      ███ 15 (vs 11)                  | |
| +-----------------------------------------------+ +--------------------------------------------+ |
|                                                                                                  |
| TECHNOLOGY RADAR & HYPE VS. ADOPTION MATRIX                                                      |
| +-----------------------+-----------------------+-----------------------+----------------------+ |
| | 🌱 EMERGING           | 🚀 RISING             | 🏛️ ESTABLISHED        | 📉 DECLINING         | |
| | • Test-Time Compute   | • Small Vision LMs    | • Standard LoRA       | • Pure RNN Baselines | |
| |   [High Attention /   |   [Balanced Paper +   |   [High Repo Growth]  |   [-18% 30d volume]  | |
| |    Low Code ⚠️ Hype]  |    GitHub Velocity]   |                       |                      | |
| +-----------------------+-----------------------+-----------------------+----------------------+ |
+--------------------------------------------------------------------------------------------------+
```

---

### Page 3: Item Deep-Dive View (`/item/:id`)
**Purpose:** Comprehensive evidence inspection for a single paper, repository, or article, connecting claims to source text and explaining the supervised ML forecast.

#### Visual Layout (2-Column Asymmetric Split):
```text
+--------------------------------------------------------------------------------------------------+
| ← Back to Feed                                              [Open Original on arXiv ↗] [PDF ↗]   |
|                                                                                                  |
| Sparse-MoE Scaling Laws for Edge-Deployed Vision Transformers                                    |
| Authors: A. Sharma, K.chen, R. Patel · Submitted: Oct 25, 2026 · Primary Domain: NLP (91%)       |
| [🔗 Linked Implementation: github.com/sharma-lab/edge-moe (★ 412 · +89 this week)]               |
+----------------------------------------------------+---------------------------------------------+
| LEFT COLUMN (60% Width): EVIDENCE & SYNTHESIS      | RIGHT COLUMN (40% Width): ML PREDICTION     |
|                                                    |                                             |
| 1. EXECUTIVE SUMMARY & CLAIMED CONTRIBUTIONS       | PREDICTED IMPACT SCORE                      |
|    • Plain-English 3-sentence synthesis...         |         ╭───────────╮                       |
|    • Key Takeaways (Bulleted)...                   |         │  8.7 / 10 │  (Top 10% Cohort)     |
|                                                    |         ╰───────────╯                       |
| 2. WHY IT MATTERS & REAL-WORLD APPLICATIONS        | Target: log(1 + 180-day citations)          |
|    • Contextual impact statement...                | Model: XGBoost v1.2 (RMSE: 0.17)            |
|                                                    |                                             |
| 3. LIMITATIONS & CANDIDATE RESEARCH GAPS           | TOP CONTRIBUTING FEATURES (Explainability)  |
|    (TechPulse Opportunity Detector)                | • Has Code Link in Abstract    [+2.4 pts]   |
|    • Evaluated only on static image classification;| • Max Author h-Index (42)      [+1.9 pts]   |
|      video temporal consistency remains untested.  | • Domain Velocity (Multimodal) [+1.1 pts]   |
|    • Candidate Direction: Test dynamic token       | • Flesch Readability (54.2)    [+0.4 pts]   |
|      pruning under thermal throttling on edge SoCs.|                                             |
|                                                    | 180-DAY PROJECTED TRAJECTORY (AreaChart)    |
| 4. ORIGINAL ABSTRACT / README SNIPPET              |   ^         ..--''"" (90% CI Band)          |
|    [Collapsible raw source text for verification]  |   |    ..--'                                |
|                                                    |   +-------------------------> Days          |
|                                                    |                                             |
|                                                    | SOURCE METADATA TABLE                       |
|                                                    | Citations: 4 | Influential: 1 | Read: 12m   |
+----------------------------------------------------+---------------------------------------------+
```

---

### Page 4: System Health & Model Evaluation (`/evaluation`)
**Purpose:** Dedicated transparency dashboard for **Persona 3 (Faculty Reviewers — Hitesh, Naman, Ritisha)** to verify every rubric metric ($\ge 85\%$ classification accuracy, $\text{RMSE} \le 0.20$, live ingestion health) during the 5-minute live evaluation.

#### Visual Layout:
```text
+--------------------------------------------------------------------------------------------------+
| SYSTEM TELEMETRY & MODEL EVALUATION (Faculty Review Dashboard)          [🔄 Trigger Manual Scan] |
+--------------------------------------------------------------------------------------------------+
| PIPELINE HEALTH (/api/health)                                                                    |
| [● PostgreSQL: Connected (10,420 items)] [● Redis Cache: 94% Hit Rate] [● Last Cron: 01:00 IST]  |
| Sources Ingested (24h): arXiv (210) · GitHub Repos (148) · Hacker News (44) · Enriched (210)     |
+------------------------------------------------+-------------------------------------------------+
| CLASSIFICATION BENCHMARKS (BART-large-MNLI)    | SUPERVISED ML IMPACT PREDICTOR (XGBoost)        |
| Held-out Test Set: n = 500 arXiv CS papers     | 5-Fold Cross-Validation & Time-Split Holdout    |
|                                                |                                                 |
| • Top-1 Accuracy:  87.4%  (Target: ≥ 85.0%) ✓  | • Paper Impact RMSE:  0.168 (Target: ≤ 0.20) ✓  |
| • Macro F1 Score:  0.83   (Target: ≥ 0.80)  ✓  | • Repo Growth RMSE:   0.182 (Target: ≤ 0.20) ✓  |
| • Low-Conf Flagged (<0.35): 4.2% (In Queue)    | • Baseline Comparison: +24% over Linear Reg.    |
|                                                |                                                 |
| Per-Domain Precision / Recall Table:           | PREDICTION VS. REALITY (Historical Backtest)    |
| NLP (0.91/0.89) · CV (0.90/0.88) · RL (0.85).. | [Scatter Chart: Predicted vs Observed Growth]   |
+------------------------------------------------+-------------------------------------------------+
```

---

### Global Overlay: Evidence-Grounded RAG Assistant (`<AssistantDrawer />`)
**Purpose:** Implements the ReAct / RAG Research Assistant without cluttering the main navigation. Triggered via the top-right `[✨ Ask AI]` button or `Cmd+K`.
* **Behavior:** Slides over as a `400px` right-hand drawer so users can keep reading their current feed or paper on the left.
* **Grounded Citations:** Every response includes clickable inline chips (e.g., `[arXiv:2610.14201]`, `[repo:vllm-project/vllm]`) that navigate the main viewport directly to `/item/:id`.
* **Quick Starter Prompts:**
  * *"What are the highest-impact NLP papers from the last 48 hours?"*
  * *"Which Computer Vision repos have the highest predicted 30-day star growth?"*
  * *"Summarize open limitations in recent edge-deployment papers."*

---

## 5. Component Tree, API Mapping & Team Ownership (`CODEOWNERS`)

To satisfy **F-08 (Probation Contribution Visibility)** and keep the React architecture modular, every component maps cleanly to a single responsibility and owner:

```text
frontend/src/
├── components/
│   ├── layout/
│   │   ├── AppShell.jsx               (Owner: Shadwal + Pragati)
│   │   ├── SidebarDomainFilter.jsx    (Owner: Pragati) ──▶ GET /api/domains
│   │   ├── TopCommandBar.jsx          (Owner: Shadwal) ──▶ GET /api/health, Search input
│   │   └── AssistantDrawer.jsx        (Owner: Sagnik)  ──▶ Stretch ReAct/RAG chat
│   ├── feed/
│   │   ├── TrendingBanner.jsx         (Owner: Pragati)
│   │   ├── FeedList.jsx               (Owner: Pragati) ──▶ GET /api/feed?domain=&sort=&page=
│   │   ├── ItemCard.jsx               (Owner: Pragati — CODEOWNERS)
│   │   ├── SourceBadge.jsx            (Owner: Pragati)
│   │   ├── DomainTag.jsx              (Owner: Pragati)
│   │   ├── ImpactScoreBar.jsx         (Owner: Pragati)
│   │   └── InsightPanel.jsx           (Owner: Pragati — CODEOWNERS) ──▶ GET /api/item/{id}/insights
│   ├── trends/
│   │   ├── DomainActivityLineChart.jsx(Owner: Pragati) ──▶ GET /api/trends?window=7d|30d
│   │   ├── WeeklyComparisonBarChart.jsx(Owner: Pragati)
│   │   └── TechRadarMatrix.jsx        (Owner: Pragati)
│   └── detail/
│       ├── FullInsightCard.jsx        (Owner: Pragati)
│       ├── PredictionWidget.jsx       (Owner: Pragati + Sagnik)
│       └── MetadataTable.jsx          (Owner: Shadwal)
└── pages/
    ├── DashboardPage.jsx              (Route: / & /explore/:domain & /search)
    ├── TrendsPage.jsx                 (Route: /trends — Owner: Pragati — CODEOWNERS)
    ├── ItemDetailPage.jsx             (Route: /item/:id — Owner: Pragati + Shadwal)
    └── EvaluationPage.jsx             (Route: /evaluation — Owner: Sagnik + Shadwal)
```

---

## 6. Navigation Flow & 5-Minute Faculty Demo Path

```text
[1. Land on / (Intelligence Feed)]
       │
       ├──▶ Filter by "Computer Vision" + "NLP" in Left Sidebar (Instant React Query update)
       ├──▶ Hover over Impact Score (8.7/10) to show explainable feature tooltip
       └──▶ Click "Expand AI Insights" on top card ──▶ Skeleton loader ──▶ 3-sentence summary + takeaways
              │
              ▼
[2. Click "Full Deep-Dive ↗" ──▶ /item/:id]
       │
       ├──▶ Inspect Paper-to-GitHub Repository link & candidate research gaps
       └──▶ Inspect ScoreGauge & 180-day citation growth projection chart
              │
              ▼
[3. Click "Trends & Radar" in Left Sidebar ──▶ /trends]
       │
       └──▶ Show 7d/30d Recharts domain velocity + Emerging vs. Hype Technology Radar
              │
              ▼
[4. Click "Model Evaluation" in Left Sidebar ──▶ /evaluation]
       │
       └──▶ Conclude demo by showing live ingestion timestamp, ≥85% BART accuracy, and ≤0.20 XGBoost RMSE
```