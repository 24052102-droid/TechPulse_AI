# ATIP (TechPulse AI) — Minimalist UI Design System & Stitch Specification

**Project:** Autonomous Technical Intelligence & Prediction Platform (ATIP / TechPulse AI)  
**Target Generator:** Stitch (AI UI / Frontend Design-to-Code Engine)  
**Aesthetic Direction:** Swiss Editorial Minimalism · High-Contrast Monochrome Base · Soft Pastel Semantic Accents  
**Design Inspirations:** Linear (Light Mode), Vercel Geist Design System, Semantic Scholar, Stripe Docs, Read.cv  

---

## 1. Master Directive for Stitch (System Prompt Context)

> **Instruction for Stitch:**  
> Design a clean, ultra-minimalist desktop-first web application for an AI/ML Technical Intelligence Platform called **ATIP (TechPulse AI)**. The interface must prioritize **signal over noise** and **progressive disclosure**.  
> - **Primary Canvas:** Pure White (`#FFFFFF`) and Alabaster (`#FAFAFA`) backgrounds.  
> - **Secondary Structure:** Deep Carbon Black (`#09090B`) for primary typography, active states, and primary CTAs, paired with crisp `1px solid #E4E4E7` hairline borders instead of heavy drop shadows.  
> - **Soft Accent Colors:** Use muted, low-saturation pastel fills with high-contrast dark tinted text for semantic signals (Domain tags, ML Impact Scores, LLM Synthesis highlights, and Trend indicators).  
> - **Information Density:** Spacious, breathable editorial layout. Never clutter cards—show only 4 core signals by default and tuck deep AI summaries inside an expandable drawer.

---

## 2. Color System & Design Tokens

### 2.1 Core Monochrome Palette (Primary White & Secondary Black)

| Token Name | Hex Code | Tailwind Equivalent | Usage Rule |
| :--- | :--- | :--- | :--- |
| `--bg-canvas` | `#FFFFFF` | `bg-white` | Primary page background and default card surface |
| `--bg-subtle` | `#FAFAFA` | `bg-zinc-50` | Sidebar background, collapsed panels, and secondary containers |
| `--bg-muted` | `#F4F4F5` | `bg-zinc-100` | Hover states on list items, segmented control tracks, skeleton loaders |
| `--ink-primary` | `#09090B` | `text-zinc-950` | Primary headings, paper/repo titles, active navigation, primary buttons |
| `--ink-secondary` | `#52525B` | `text-zinc-600` | Body copy, LLM summaries, abstract excerpts, secondary descriptions |
| `--ink-tertiary` | `#A1A1AA` | `text-zinc-400` | Timestamps, arXiv IDs, keyboard shortcuts (`⌘K`), axis labels |
| `--border-hairline` | `#E4E4E7` | `border-zinc-200` | All structural grid dividers, card borders, and table rules (`1px solid`) |
| `--border-focus` | `#09090B` | `border-zinc-950` | Active input focus rings, selected card outlines, active tab indicators |

### 2.2 Soft Accent Palette (Semantic Signals & Data Visualization)

All accent colors follow a **Soft Surface + Crisp Border + Deep Tint Text** formula so they remain gentle on the eyes against the `#FFFFFF` canvas while maintaining WCAG AAA readability.

| Signal / Purpose | Soft Fill (`bg`) | Subtle Border (`border`) | Accent Text / Icon (`text`) | Chart / Bar Solid (`fill`) | Usage in ATIP |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **LLM Intelligence (Soft Indigo)** | `#EEF2FF` (`indigo-50`) | `#E0E7FF` (`indigo-100`) | `#4338CA` (`indigo-700`) | `#6366F1` (`indigo-500`) | Expandable `InsightPanel` accent, "Why It Matters" callout, AI Assistant trigger |
| **High Impact Score ($8.0 - 10.0$) (Soft Sage)** | `#ECFDF5` (`emerald-50`) | `#D1FAE5` (`emerald-100`) | `#047857` (`emerald-700`) | `#10B981` (`emerald-500`) | High-signal impact bars, "Rising" trend badges, verified code links |
| **Moderate Impact ($5.0 - 7.9$) (Soft Amber)** | `#FFFBEB` (`amber-50`) | `#FEF3C7` (`amber-100`) | `#B45309` (`amber-700`) | `#F59E0B` (`amber-500`) | Mid-tier impact scores, "Emerging" radar quadrant, 48h velocity spike badge |
| **Low Confidence / Hype Alert (Soft Rose)** | `#FFF1F2` (`rose-50`) | `#FFE4E6` (`rose-100`) | `#BE123C` (`rose-700`) | `#F43F5E` (`rose-500`) | Low classification confidence ($< 35\%$), "High Hype / Low Adoption" warning |
| **Domain / Technical Tag (Soft Slate Sky)** | `#F0F9FF` (`sky-50`) | `#E0F2FE` (`sky-100`) | `#0369A1` (`sky-700`) | `#0EA5E9` (`sky-500`) | Primary domain classification pills (NLP, CV, Robotics, Systems) |
| **Research Opportunity (Soft Violet)** | `#F5F3FF` (`violet-50`) | `#EDE9FE` (`violet-100`) | `#6D28D9` (`violet-700`) | `#8B5CF6` (`violet-500`) | Candidate research gap cards, paper-to-repo semantic match badges |

### 2.3 Source Badge Accents

| Source | Pill Background | Pill Border | Text & Icon Color | Icon Style |
| :--- | :--- | :--- | :--- | :--- |
| **arXiv Paper** | `#FFF1F2` | `#FFE4E6` | `#9F1239` | Minimal `FileText` icon |
| **GitHub Repo** | `#F4F4F5` | `#E4E4E7` | `#09090B` | Minimal `GitBranch` icon |
| **Hacker News** | `#FFF7ED` | `#FFEDD5` | `#C2410C` | Minimal `Flame` or `MessageSquare` icon |

---

## 3. Typography & Hierarchy

Use a dual-font pairing: a clean neo-grotesque sans-serif for editorial reading and a crisp monospace font for all ML metrics, scores, and timestamps.

*   **Primary UI & Editorial Font:** `Inter` or `Geist Sans`
*   **Technical & Metric Font:** `JetBrains Mono` or `Geist Mono` (mandatory for all numbers, percentages, RMSE/F1 scores, and IDs)

| Element | Font Family | Size (`px` / `rem`) | Weight | Line Height | Letter Spacing | Color |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Page Title (H1)** | Sans | `24px` (`1.5rem`) | `600` (SemiBold) | `1.3` | `-0.025em` | `#09090B` |
| **Section Header (H2)** | Sans | `16px` (`1.0rem`) | `600` (SemiBold) | `1.4` | `-0.015em` | `#09090B` |
| **Item Card Title (H3)** | Sans | `16px` (`1.0rem`) | `500` (Medium) | `1.45` | `-0.01em` | `#09090B` (Hover: `#4338CA`) |
| **Body / LLM Summary** | Sans | `14px` (`0.875rem`) | `400` (Regular) | `1.65` | `0em` | `#52525B` |
| **Sidebar / UI Label** | Sans | `13px` (`0.8125rem`) | `500` (Medium) | `1.4` | `0em` | `#09090B` |
| **Micro Overline** | Mono | `11px` (`0.6875rem`) | `600` (SemiBold) | `1.2` | `+0.06em` (Uppercase) | `#A1A1AA` |
| **Impact Score Metric** | Mono | `14px` (`0.875rem`) | `600` (SemiBold) | `1.0` | `-0.02em` | `#09090B` |
| **KPI Big Number** | Mono | `28px` (`1.75rem`) | `600` (SemiBold) | `1.1` | `-0.03em` | `#09090B` |

---

## 4. Spatial Grid, Borders & Elevation Rules

1.  **Zero-Shadow Philosophy:** Do not use blurry drop shadows (`shadow-lg`, `shadow-xl`) on cards. Achieve depth using:
    *   `1px solid #E4E4E7` borders on a `#FFFFFF` surface.
    *   Subtle border darkening on hover (`hover:border-zinc-400` or `hover:border-zinc-950`).
    *   Soft background shifts (`#FFFFFF` $\rightarrow$ `#FAFAFA`) for nested panels.
    *   *Exception:* Only floating tooltips and the slide-over RAG drawer may use a crisp subtle shadow (`0 8px 30px rgba(0, 0, 0, 0.06)`).
2.  **Border Radius Scale:**
    *   Outer Cards & Containers: `12px` (`rounded-xl`)
    *   Buttons, Inputs & Inner Panels: `8px` (`rounded-lg`)
    *   Domain Tags & Badges: `6px` (`rounded-md`) or full pill (`rounded-full`)
3.  **Application Shell Dimensions:**
    *   **Left Navigation & Filter Sidebar:** Fixed `248px` width, `bg-[#FAFAFA]`, right border `1px solid #E4E4E7`, full viewport height (`100vh`), sticky.
    *   **Top Command Header:** Fixed `56px` height, `bg-white/85` with `backdrop-blur-md`, bottom border `1px solid #E4E4E7`, sticky.
    *   **Main Content Area:** Fluid width with a centered inner container (`max-w-[1080px]`, `px-8`, `py-6`) so lines of text never exceed comfortable reading width.

---

## 5. Component Specifications for Stitch

### 5.1 `TopCommandBar` (Sticky Global Header)
*   **Layout:** Horizontal flex container (`h-14 px-6 border-b border-zinc-200 bg-white flex items-center justify-between gap-4`).
*   **Left Zone (Search Input):**
    *   Minimalist search bar (`w-96 h-9 px-3 rounded-lg bg-zinc-50 border border-zinc-200 focus-within:border-zinc-950 focus-within:bg-white`).
    *   Left `Search` icon (`14px`, `#A1A1AA`), placeholder `"Search papers, repos, or methods..."`, right keyboard badge `⌘K` in monospace (`text-[11px] bg-white border border-zinc-200 px-1.5 py-0.5 rounded`).
*   **Center Zone (Segmented Sort Pill):**
    *   Track container: `bg-zinc-100 p-0.5 rounded-lg inline-flex items-center`.
    *   3 Options: `Impact Score` | `Trending` | `Latest`.
    *   Active pill: `bg-white text-zinc-950 shadow-none border border-zinc-200/80 rounded-md px-3 py-1 text-xs font-medium`.
*   **Right Zone (System Status & AI Trigger):**
    *   **Pipeline Status Indicator:** Soft emerald dot (`w-2 h-2 rounded-full bg-emerald-500`) + monospace text `Synced 2h ago` (`text-xs text-zinc-500`).
    *   **Ask AI Button (Primary Black CTA):** `bg-zinc-950 hover:bg-zinc-800 text-white text-xs font-medium px-3.5 py-2 rounded-lg inline-flex items-center gap-1.5` with a subtle `Sparkles` icon in soft indigo (`#A5B4FC`).

### 5.2 `LeftSidebar` (Navigation & Domain Taxonomy Filter)
*   **Layout:** Vertical flex column (`w-[248px] bg-[#FAFAFA] border-r border-zinc-200 p-4 flex flex-col justify-between select-none`).
*   **Brand Header:**
    *   Minimal geometric cube or pulse mark in solid black (`w-6 h-6 rounded-md bg-zinc-950 text-white flex items-center justify-center font-mono text-xs font-bold` $\rightarrow$ `AT`) + Title `ATIP` (`font-semibold text-sm text-zinc-950`) + subtle tag `v1.0` (`font-mono text-[11px] text-zinc-400`).
*   **Primary Navigation Group (3 Pillars):**
    *   `Intelligence Feed` (Icon: `Layers`, Route: `/`)
    *   `Trends & Radar` (Icon: `Activity`, Route: `/trends`)
    *   `Model Evaluation` (Icon: `ShieldCheck`, Route: `/evaluation`)
    *   *Active State:* `bg-zinc-950 text-white rounded-lg px-3 py-2 text-xs font-medium`.
    *   *Inactive State:* `text-zinc-600 hover:bg-zinc-200/60 hover:text-zinc-950 rounded-lg px-3 py-2 text-xs font-medium`.
*   **Source Filter Pills (Horizontal 4-way toggle):**
    *   `All` | `arXiv` | `GitHub` | `HN` (`text-[11px] font-mono py-1 px-2 rounded-md border`).
*   **Domain Taxonomy List (10 Checkboxes):**
    *   Section label: `DOMAINS` (`font-mono text-[11px] uppercase tracking-wider text-zinc-400 mb-2`).
    *   Each row (`py-1.5 px-2 rounded-md hover:bg-zinc-100 flex items-center justify-between cursor-pointer`):
        *   Left: Custom `14px` rounded-sm checkbox (`checked:bg-zinc-950 checked:border-zinc-950`) + Domain name (`text-xs text-zinc-700 truncate`).
        *   Right: Live item count in monospace (`text-[11px] font-mono text-zinc-400`) + tiny soft emerald dot if that domain is trending this week.

### 5.3 `TrendingBanner` (Top of Feed Bento Strip)
*   **Purpose:** Highlights the top 3 fastest-rising breakthroughs in the last 48 hours without taking up excessive vertical space.
*   **Layout:** 3-column compact horizontal grid (`grid grid-cols-3 gap-3 mb-6`).
*   **Card Style:** `bg-[#FAFAFA] border border-zinc-200 hover:border-zinc-400 rounded-xl p-3.5 transition-colors`.
*   **Internal Elements:**
    *   Top row: Soft Amber pill `🔥 Rising +42%` (`bg-amber-50 text-amber-700 border border-amber-100 text-[11px] font-mono px-2 py-0.5 rounded`) + Source label (`arXiv` / `GitHub`).
    *   Middle: 1-line truncated title (`text-xs font-medium text-zinc-950 mt-2`).
    *   Bottom: Primary Domain + Monospace Impact Score `9.4/10` (`text-emerald-700 font-mono text-xs font-semibold`).

### 5.4 `ItemCard` (Core Feed Intelligence Card)
*   **Purpose:** Displays a single paper, repository, or tech discussion with strict visual restraint.
*   **Container:** `bg-white border border-zinc-200 hover:border-zinc-300 rounded-xl p-5 mb-3 transition-all`.
*   **Row 1 — Metadata & Impact Bar (Flex Between):**
    *   **Left Group:**
        1.  `SourceBadge` (e.g., `arXiv` in soft rose or `GitHub` in crisp zinc).
        2.  `DomainTag` Primary (Soft Sky pill: `bg-sky-50 text-sky-700 border border-sky-100 text-xs px-2.5 py-0.5 rounded-md font-medium`). On hover, reveals monospace confidence `92%`.
        3.  `SecondaryDomainTag` (Neutral pill: `bg-zinc-100 text-zinc-600 text-xs px-2 py-0.5 rounded-md`).
        4.  `PaperToCodeBadge` (Conditional: if an arXiv paper has a linked GitHub implementation, show `🔗 Code Linked` in Soft Violet `bg-violet-50 text-violet-700 border border-violet-100 text-[11px] font-mono px-2 py-0.5 rounded-md`).
    *   **Right Group (`ImpactScoreWidget`):**
        *   Label `IMPACT` (`font-mono text-[10px] text-zinc-400 uppercase`).
        *   Segmented or smooth horizontal progress bar (`w-20 h-1.5 bg-zinc-100 rounded-full overflow-hidden`) with soft emerald fill (`bg-emerald-500` for $\ge 8.0$, `bg-amber-500` for $5.0 - 7.9$).
        *   Score number in monospace: `8.9` (`font-mono text-sm font-semibold text-zinc-950`) `/10`.
        *   **Hover Tooltip (Explainable AI):** Floating white card (`border border-zinc-200 p-3 rounded-lg w-64`) listing top 3 XGBoost feature drivers:
            *   `+0.34 Author h-index (48)`
            *   `+0.28 Linked GitHub repo`
            *   `+0.19 Citation velocity`
*   **Row 2 — Title:**
    *   `text-base font-medium text-zinc-950 hover:text-indigo-700 cursor-pointer mt-2.5 leading-snug`.
*   **Row 3 — Subtle Footer & Progressive Disclosure Trigger:**
    *   **Left:** Monospace metadata (`2h ago · 4 authors · 12 min read` or `★ 1,420 (+310 est. 30d) · Python`).
    *   **Right (`InsightToggleButton`):**
        *   Collapsed state: Soft Indigo ghost button (`bg-indigo-50/70 hover:bg-indigo-100/80 text-indigo-700 border border-indigo-100 rounded-lg px-3 py-1 text-xs font-medium inline-flex items-center gap-1.5`) reading `✦ AI Insights ▾`.
        *   Expanded state: Solid Black button (`bg-zinc-950 text-white rounded-lg px-3 py-1 text-xs font-medium`) reading `✦ Hide Insights ▴`.

### 5.5 `InsightPanel` (Lazy-Loaded Expandable AI Drawer inside `ItemCard`)
*   **Container:** Renders seamlessly at the bottom of `ItemCard` when expanded (`mt-4 pt-4 border-t border-zinc-200/80 bg-[#FAFAFA] -mx-5 -mb-5 p-5 rounded-b-xl`).
*   **Loading State:** 3 clean pulsing horizontal shimmer bars (`bg-zinc-200/70 h-3 rounded animate-pulse`) so the user never sees a jarring spinner.
*   **Loaded Layout (2-Column Asymmetric Grid `grid-cols-12 gap-6`):**
    *   **Left Column (7 cols — Executive Synthesis):**
        *   Overline: `LLM SYNTHESIS · CLAUDE SONNET` (`font-mono text-[10px] uppercase tracking-wider text-indigo-600 mb-1.5`).
        *   **3-Sentence Summary:** `text-sm text-zinc-700 leading-relaxed mb-4`.
        *   **Key Technical Takeaways:** 3 bullet points with crisp black square markers (`▪`) and `text-xs text-zinc-600 space-y-1.5`.
    *   **Right Column (5 cols — Significance & Context):**
        *   **"Why This Matters" Box:** Soft Indigo tinted card (`bg-indigo-50/60 border border-indigo-100 rounded-lg p-3.5`).
            *   Header: `Why It Matters` (`text-xs font-semibold text-indigo-900 mb-1`).
            *   Body: `text-xs text-indigo-950/80 leading-relaxed`.
        *   **Metadata Pills Row (Bottom of right column):**
            *   Technical Depth Badge: `Intermediate` (`bg-white border border-zinc-200 text-zinc-700 text-[11px] font-mono px-2 py-0.5 rounded`).
            *   Related Topic Chips: 3 clickable micro-tags (`#SpeculativeDecoding`, `#KV-Cache`) in `text-[11px] font-mono text-zinc-500 hover:text-zinc-950`.
        *   **Bottom Action Link:** `Open Full Deep-Dive & Forecast →` (`text-xs font-medium text-zinc-950 underline underline-offset-4 hover:text-indigo-700 mt-3 inline-block`).

---

## 6. Screen-by-Screen Visual Blueprints

### Screen 1: `/` — Intelligence Feed (Main Dashboard)
*   **Visual Hierarchy:**
    1.  `TopCommandBar` (Search + Sort + Sync pill + Ask AI).
    2.  `TrendingBanner` (Top 3 rising cards in a compact row).
    3.  Active Filter Bar (only visible if filters are active: shows removable black/pastel chips `Domain: NLP ×`, `Source: arXiv ×`, plus `Clear all`).
    4.  `FeedList` (Vertical stack of `ItemCard` components, 20 per page, with one card shown in its **Expanded `InsightPanel` state** to showcase the progressive disclosure pattern).

### Screen 2: `/trends` — Trends & Technology Radar
*   **Header:** Title `Domain Velocity & Technology Radar` + Window Toggle (`7 Days` | `30 Days` | `90 Days`).
*   **Section A — Technology Radar (4-Quadrant Minimalist Bento Grid `grid-cols-4 gap-4`):**
    *   Quadrant 1: **Emerging** (Soft Violet accent `#F5F3FF`) — High research growth, early repos.
    *   Quadrant 2: **Rising** (Soft Sage accent `#ECFDF5`) — Steepest positive 7-day slope (`+28% WoW`).
    *   Quadrant 3: **Established** (Soft Sky accent `#F0F9FF`) — High volume, stable baseline.
    *   Quadrant 4: **Declining / Saturated** (Neutral Zinc `#F4F4F5`) — Slowing momentum.
    *   *Each Quadrant Card* lists 2–3 domain/topic rows with monospace sparklines and WoW delta percentages.
*   **Section B — Charts Row (`grid-cols-12 gap-6 mt-6`):**
    *   **Left (7 cols) — Domain Activity Line Chart:** White card (`border border-zinc-200 rounded-xl p-5`). Ultra-clean Recharts line graph with dashed `#F4F4F5` horizontal gridlines, no vertical gridlines, and 4 smooth `2px` strokes (`#09090B` Black, `#6366F1` Soft Indigo, `#10B981` Emerald, `#F59E0B` Amber).
    *   **Right (5 cols) — Hype vs. Adoption Matrix:** Compares **Paper Mention Growth (X-axis)** vs. **GitHub Star/Commit Velocity (Y-axis)**. Flags outliers with a Soft Rose pill (`⚠️ High Hype / Low Code Adoption`).

### Screen 3: `/item/:id` — Item Deep-Dive & Explainable Forecast
*   **Top Breadcrumb:** `← Back to Intelligence Feed` + Source External Button (`View on arXiv ↗` or `View on GitHub ↗` in secondary black outline).
*   **2-Column Split Layout (`grid-cols-12 gap-8`):**
    *   **Left Column (7 cols — Grounded Evidence & LLM Analysis):**
        *   Full Title (`24px SemiBold #09090B`), Authors/Contributors list, Publication timestamp, and Domain tags.
        *   **Paper-to-Repository Card (if matched):** Crisp callout card linking the paper directly to its verified GitHub implementation with live star/fork counters.
        *   **Structured LLM Analysis Sections:** Clean white card divided by `1px solid #E4E4E7` hairlines into:
            1.  *Executive Summary*
            2.  *Core Contributions & Methodology* (with `[Abstract, §2]` source provenance tags)
            3.  *Reported Limitations & Caveats* (highlighted in subtle Soft Amber `#FFFBEB`)
            4.  *Candidate Research Opportunities* (highlighted in subtle Soft Violet `#F5F3FF` — suggests 2 follow-up research questions).
    *   **Right Column (5 cols — Supervised ML Prediction & Feature Attribution):**
        *   **Explainable Impact Forecast Card (`bg-[#FAFAFA] border border-zinc-200 rounded-xl p-5`):**
            *   Top metric: Monospace `8.9 / 10` Impact Score + Target Horizon badge (`180-Day Citation Forecast` or `90-Day Star Growth`).
            *   **Growth Trajectory Area Chart:** Minimal Recharts area curve showing historical baseline (solid black line) + predicted 90-day growth cone (dashed emerald line with soft `#ECFDF5` shaded confidence band).
            *   **SHAP / Feature Attribution Bars:** Horizontal positive/negative contribution bars showing *why* the XGBoost model predicted this score (e.g., `Author Max h-Index`, `Code Availability`, `Readability Score`).

### Screen 4: `/evaluation` — System Health & Model Evaluation (Faculty Demo View)
*   **Purpose:** Built specifically for the KIIT IoT Lab leadership review to prove ML rigor, accuracy targets, and pipeline health.
*   **Top Row — 4 KPI Metric Cards (`grid-cols-4 gap-4`):**
    1.  **Classification Top-1 Accuracy:** `88.4%` (Target: $\ge 85\%$, Soft Sage badge `✓ Passing`).
    2.  **Macro F1 Score:** `0.83` (Target: $\ge 0.80$, model: `BART-large-MNLI`).
    3.  **Impact Prediction RMSE:** `0.16` (Target: $\le 0.20$, 5-fold CV on normalized $0-1$ scale).
    4.  **Ingestion & Cache Health:** `100%` LLM coverage · `74%` Redis cache hit rate.
*   **Middle Row (`grid-cols-12 gap-6`):**
    *   **Left (6 cols) — Per-Domain Precision & Recall Table:** Clean monochrome table with subtle inline horizontal progress bars for all 10 domains.
    *   **Right (6 cols) — Prediction vs. Reality Calibration Plot:** Scatter/line comparison showing historical predicted scores against actual observed 6-month citations/stars, plus a toggleable **"Known Failure Modes"** sample table showing transparency.

### Global Overlay: `RagAssistantDrawer` (Evidence-Grounded Chat Slide-Over)
*   **Trigger:** Clicking `✦ Ask AI` in the top bar slides out a `420px` right-hand drawer (`bg-white border-l border-zinc-200 shadow-2xl`).
*   **Design:**
    *   Header: `Evidence-Grounded Assistant` + scope badge `Searching 1,420 indexed papers & repos`.
    *   Suggested Starter Prompts (soft zinc pills): `"What are the top NLP papers this week?"`, `"Compare top 2 Vision repos"`, `"What limitations recur in RAG papers?"`.
    *   Assistant Responses: Clean markdown text with inline clickable citation pills (`[arXiv:2610.0412]`, `[github:vllm-project]`) in Soft Indigo (`#EEF2FF`).

---

## 7. Copy-Paste Prompts for Stitch (Screen-by-Screen Generation)

Use the prompts below directly inside **Stitch** to generate each screen with 100% visual consistency.

### Prompt 1: Main Intelligence Feed (`/`)
```text
Create a minimalist desktop web application screen for "ATIP (TechPulse AI) - Technical Intelligence Feed".
Aesthetic: Ultra-minimalist Swiss grid, pure white (#FFFFFF) primary background, soft alabaster (#FAFAFA) sidebar, deep black (#09090B) primary typography and active buttons, 1px solid #E4E4E7 hairline borders, zero drop shadows, and soft pastel semantic accents. Font pairing: Inter for UI/editorial text and JetBrains Mono for metrics, scores, and IDs.

Layout Structure:
1. Fixed Left Sidebar (248px wide, #FAFAFA background, 1px right border #E4E4E7):
   - Brand header with a solid black geometric badge "AT" and title "ATIP v1.0".
   - 3 navigation links: "Intelligence Feed" (active, solid #09090B black background with white text), "Trends & Radar", and "Model Evaluation".
   - Source filter segmented row: All | arXiv | GitHub | HN.
   - "DOMAINS" checklist section with 10 technical domains (Natural Language Processing, Computer Vision, Reinforcement Learning, IoT & Embedded, Systems & Infra, Robotics, Security, General ML, Data Engineering, Multimodal AI), each showing a minimal checkbox and a monospace item count on the right.

2. Sticky Top Command Header (56px high, #FFFFFF background, 1px bottom border #E4E4E7):
   - Left: Minimal search input ("Search papers, repos, or methods...") with a monospace "⌘K" shortcut badge.
   - Center: Segmented sort pill control ("Impact Score" active, "Trending", "Latest").
   - Right: Live pipeline status indicator (emerald dot + "Synced 2h ago" in monospace) and a solid black CTA button "✦ Ask AI".

3. Main Content Container (centered, max-width 1040px, generous padding):
   - Top "48h Breakout Signals" bento strip: 3 compact horizontal cards (#FAFAFA bg, 1px border) showing a soft amber badge ("🔥 +38% velocity"), title, domain tag, and monospace impact score ("9.4/10").
   - Vertical Feed List of 4 Intelligence Item Cards (#FFFFFF bg, 1px solid #E4E4E7 border, 12px border radius, 20px padding):
     - Card Top Row: Source badge (arXiv in soft rose #FFF1F2 or GitHub in soft zinc #F4F4F5), Primary Domain tag in soft sky blue (#F0F9FF fill, #0369A1 text, "94%" confidence), "🔗 Code Linked" badge in soft violet (#F5F3FF), and on the right an Explainable Impact Score widget showing a horizontal emerald progress bar and "9.1 / 10" in JetBrains Mono.
     - Card Middle: Crisp 16px medium-weight title in #09090B.
     - Card Footer: Monospace metadata ("3h ago · 5 authors · 10 min read") on the left, and a soft indigo pill button "✦ AI Insights ▾" (#EEF2FF fill, #4338CA text) on the right.
     - Show the SECOND card in its EXPANDED state: reveal a bottom attached drawer (#FAFAFA background, top 1px border) split into 2 columns: Left column has a 3-sentence plain-English LLM summary and 3 bulleted technical takeaways; Right column has a soft indigo callout box ("Why This Matters" in #EEF2FF) plus "Advanced" depth badge and 3 monospace topic tags.
```

### Prompt 2: Trends & Technology Radar (`/trends`)
```text
Create a minimalist desktop web screen for "ATIP - Trends & Technology Radar" matching the exact same Left Sidebar and Top Command Header as the main dashboard.
Aesthetic: Pure white (#FFFFFF) canvas, #FAFAFA secondary containers, #09090B black typography, 1px solid #E4E4E7 borders, Inter + JetBrains Mono fonts, soft pastel accents.

Main Content Area:
1. Page Header: Title "Domain Velocity & Technology Radar" on the left, and a segmented time-window toggle ("7D" | "30D" | "90D") on the right.
2. Technology Radar 4-Quadrant Grid (4 equal columns, 12px radius cards):
   - "Emerging" card with Soft Violet header pill (#F5F3FF fill, #6D28D9 text)
   - "Rising" card with Soft Sage Emerald header pill (#ECFDF5 fill, #047857 text)
   - "Established" card with Soft Sky Blue header pill (#F0F9FF fill, #0369A1 text)
   - "Cooling" card with Neutral Zinc header pill (#F4F4F5 fill, #52525B text)
   Each quadrant lists 3 technical topics with mini sparklines and monospace week-over-week growth percentages (e.g., "+34%").
3. Two-Column Analytics Row below:
   - Left (7 columns): "30-Day Domain Activity Volume" clean minimalist line chart card with subtle dashed horizontal gridlines and 4 crisp lines (#09090B Black, #6366F1 Indigo, #10B981 Emerald, #F59E0B Amber).
   - Right (5 columns): "Hype vs. Adoption Signal Matrix" card comparing Paper Volume Growth vs. GitHub Star Growth, featuring a Soft Rose warning badge ("⚠️ High Research Hype / Low Code Adoption") on outlier topics.
```

### Prompt 3: Item Deep-Dive & Forecast (`/item/:id`)
```text
Create a minimalist desktop web screen for "ATIP - Item Deep-Dive & Explainable Impact Forecast".
Aesthetic: Pure white (#FFFFFF) primary surface, #FAFAFA secondary cards, #09090B black accents, 1px solid #E4E4E7 hairline borders, Inter + JetBrains Mono typography, and soft pastel semantic highlights.

Main Content Area (2-Column Asymmetric Split, 12-column grid):
1. Top Breadcrumb row: "← Back to Intelligence Feed" link on the left, and two crisp action buttons on the right: "View arXiv PDF ↗" (white outline) and "Open Linked GitHub Repo (★ 1.8k) ↗" (solid #09090B black button).
2. Left Column (7 columns - Grounded LLM Synthesis):
   - Source badge (arXiv), Domain pills (Multimodal AI, Systems), Title in 24px SemiBold #09090B, author list, and submission date.
   - Structured Analysis Card (#FFFFFF bg, 1px border #E4E4E7) divided by hairline rules into:
     a) Executive Summary (3 crisp sentences)
     b) Key Technical Contributions & Methodology (bulleted list with inline monospace provenance citations like "[Section 3.2]")
     c) Reported Limitations (subtle Soft Amber callout #FFFBEB)
     d) Candidate Research Opportunities (subtle Soft Violet callout #F5F3FF listing 2 open follow-up research questions).
3. Right Column (5 columns - Supervised ML Forecast & Explainability):
   - Impact Prediction Card (#FAFAFA bg, 1px border #E4E4E7, 12px radius):
     - Header showing "PREDICTED IMPACT SCORE" and large monospace metric "9.2 / 10" with a Soft Sage Emerald badge "Top 5% Decile".
     - Area Chart showing "180-Day Citation / Star Growth Forecast" with a solid black historical line and a dashed emerald forecast curve inside a soft emerald confidence band (#ECFDF5).
     - "XGBoost Feature Attribution (Why this score?)" section showing 4 horizontal contribution bars in monospace: Author Max h-Index (+0.38), Linked GitHub Implementation (+0.29), Abstract Readability (+0.15), Domain Momentum (+0.10).
```

### Prompt 4: Model Evaluation & System Health (`/evaluation`)
```text
Create a minimalist desktop web screen for "ATIP - Model Evaluation & Pipeline Telemetry" designed for an academic faculty review demo.
Aesthetic: Pure white (#FFFFFF) canvas, #FAFAFA secondary cards, #09090B black typography, 1px solid #E4E4E7 hairline borders, JetBrains Mono for all metrics.

Main Content Area:
1. Header: "ML Evaluation & Pipeline Telemetry" with a live green status pill "All Pipeline Workers Healthy" and a black outline button "Trigger Manual Scan".
2. Top KPI Row (4 cards in a row, #FFFFFF bg, 1px border):
   - "Classification Accuracy": 88.4% in 28px JetBrains Mono + Soft Emerald pill "Target ≥ 85% Met"
   - "Macro F1 Score": 0.83 in 28px JetBrains Mono + "BART-large-MNLI (500-item test set)"
   - "Impact Prediction RMSE": 0.16 in 28px JetBrains Mono + Soft Emerald pill "Target ≤ 0.20 Met (5-Fold CV)"
   - "LLM Cache Efficiency": 76.2% in 28px JetBrains Mono + "Redis SHA-256 Cache · ₹180/mo spend"
3. Bottom Split Row (2 equal columns):
   - Left Card: "Per-Domain Classification Performance" clean minimalist table listing the 10 domains with Precision, Recall, F1-score in monospace and thin black/indigo inline progress bars.
   - Right Card: "Forecast vs. Observed Reality (Backtest Calibration)" scatter/line plot comparing predicted impact vs actual 180-day citations/stars, with a bottom collapsible drawer showing 2 "Low-Confidence / Error Case Studies" in Soft Rose (#FFF1F2) for model transparency.
```