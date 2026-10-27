ATIP Platform

PRD · TRD · Workflow · v1.0

Overview

[Cover](#cover) [Executive Summary](#exec-summary) [Problem Statement](#problem) [Goals & Metrics](#goals) [Personas & Use Cases](#personas)

PRD

[Feature Set](#features) [Non-Functional Req.](#nfr) [Priority Matrix](#priority)

TRD

[System Architecture](#architecture) [Data Ingestion Layer](#ingestion) [Classification Layer](#classification) [LLM / Agent Layer](#llm) [ML Prediction Layer](#prediction) [Frontend Layer](#frontend) [DB Schema & API](#schema)

Workflow

[End-to-End Data Flow](#e2e-workflow) [User Request Flow](#user-flow)

Execution

[Tech Stack](#tech-stack) [Team & Sprint Plan](#team) [Risk Register](#risks)

IoT Lab — Machine Learning · Campus 25, KIIT University

# Autonomous Technical Intelligence & Prediction Platform

PRD TRD Workflow v1.0 · October 2026 Project POC: Sagnik Pramanik

01

## Executive Summary

The **Autonomous Technical Intelligence Platform (ATIP)** is a web-based system that continuously ingests unstructured and structured data from multiple technical content sources — research papers, open-source repositories, and tech news feeds — and transforms them into classified, impact-scored, and LLM-synthesized intelligence cards.

The platform addresses a fundamental problem in the developer and researcher community: the daily volume of technical content (2000+ arXiv papers, 90,000+ new GitHub repos) makes it practically impossible to manually track high-signal outputs. ATIP solves this by combining zero-shot domain classification, supervised ML-based impact prediction, and LLM-generated insight synthesis into a single interactive web interface.

Built for the IoT Lab — Machine Learning vertical at KIIT University (Campus 25), ATIP is evaluated on three dimensions: a working, demonstrable web platform; a clean shared GitHub repository with traceable contributions; and a live, faculty-ready demo showing classification accuracy, prediction scores, and LLM-generated insights across multiple technical domains.

3+

Data source types ingested

10

Technical domains classified

≥85%

Classification accuracy target

≤0.2

Impact prediction RMSE

02

## Problem Statement & Context

### The Information Overload Gap

The pace of technical publication has outrun human capacity to filter. Every 24 hours, the global tech community produces thousands of new research papers, open-source project releases, and technical discussions. The ratio of signal to noise is deteriorating rapidly, and existing tools fail to solve this in a meaningful way:

- arXiv publishes \~2,000 new papers daily across CS categories alone
- GitHub sees 90,000+ new repository creations per day globally
- Developers and students spend 2–4 hours per day just attempting to filter relevant content
- Existing aggregators (Hacker News, Papers With Code) surface popularity — not predicted quality or impact
- No single platform combines domain classification + impact prediction + LLM-generated synthesis

### Who Is Affected

- **ML/AI researchers and students** who need to stay current on new methods without reading every abstract
- **Open-source developers** who want to identify high-signal repositories before they trend
- **Lab teams and academic groups** (like the IoT Lab at KIIT) that need structured intelligence to guide their own research directions

### The Missing Solution

- An automated pipeline that goes from raw content to structured, domain-tagged insight in one pass
- A prediction layer that assigns a quantitative quality/impact score to each piece of content — not just star counts or citation counts after the fact, but early-stage predictions
- Cross-source synthesis: connecting a paper, its GitHub implementation, and the community discussion around it in one view
- A platform accessible via browser with no friction — no login, no setup — for demo and daily use

**Scope Note** The problem is explicitly open-ended per the project brief. The team has full freedom to decide data sources, model choices, and architecture. This PRD makes deliberate, reasoned choices in each area, but those choices can be revised by the POC during sprint planning.

03

## Goals, Success Metrics & Scope

### Product Goals

1. Build a fully functional, live-accessible web platform ready for faculty review
2. Ingest and process content from at least 3 distinct source types (papers, repos, articles)
3. Classify all items into a domain taxonomy of ≥ 8 technical domains with ≥ 85% top-1 accuracy
4. Generate LLM-synthesized summaries and insight bullets for every classified item
5. Predict impact or growth scores using supervised ML with measurable accuracy (RMSE ≤ 0.2)
6. Maintain a clear, contribution-tracked shared GitHub repository

### Technical Goals

1. Ingestion pipeline running on an automated cron schedule with daily refresh
2. Classification model deployed as an API-callable service
3. LLM API calls cached and batched to manage cost within lab budget
4. Frontend renders a paginated feed with sub-2s load time on 4G
5. Deployment to a free-tier cloud provider; URL shareable with faculty before review

### Success Metrics

| Metric | Target | Measurement Method |
| --- | --- | --- |
| Classification top-1 accuracy | ≥ 85% | Held-out test set of 500 arXiv papers with known categories |
| Classification macro F1 | ≥ 0.80 | Scikit-learn classification_report on test set |
| Impact score prediction RMSE | ≤ 0.20 (normalized 0–1) | 5-fold cross-validation on historical dataset |
| LLM insight coverage | 100% of P0 items | DB check: insights table completeness |
| Frontend load time (feed page) | \< 2s on 4G | Chrome DevTools Lighthouse audit |
| API response time (search) | \< 500ms p95 | FastAPI middleware timing logs |
| GitHub contributions | All 4 members have ≥ 10 commits each | GitHub contribution graph |

### Out of Scope (v1)

- Real-time streaming ingestion (websockets, Kafka)
- User authentication, user accounts, or personalized feeds
- Mobile native application (iOS/Android)
- Paid/premium tiers or monetization features
- Fine-tuning a custom LLM from scratch
- Integration with institutional databases (Scopus, IEEE Xplore) — licensing barriers
- Email digest / notification system (stretch, Sprint 4 only if time permits)

PRD

## User Personas & Use Cases

### Primary Personas

#### Persona 1 — The ML Researcher/Student (Primary)

**Aryan · 3rd-year BTech CS, KIIT** Goal: Stay current on NLP and Computer Vision papers without spending hours on arXiv. Pain point: Can't distinguish impactful papers from incremental ones at a glance. No time to check GitHub for implementations. How they use ATIP: Opens dashboard → filters by "NLP" → sorts by Impact Score → reads 3–5 LLM summaries → notes 2 papers for deeper reading.

#### Persona 2 — The Open-Source Developer (Secondary)

**Meera · Independent developer** Goal: Find early-stage, high-signal GitHub repositories before they blow up in popularity. Pain point: GitHub Trending shows popularity, not quality. Hacker News is noisy. How they use ATIP: Goes to "Repositories" tab → sorts by predicted 30-day star growth → identifies repos to watch and contribute to early.

#### Persona 3 — Faculty Reviewer (Evaluation)

**Hitesh Singh / Naman Singh / Ritisha · IoT Lab Leadership Board** Goal: Assess whether the team has built a real, functional ML + LLM + prediction system. How they use ATIP: Navigate to live URL → explore domain classification accuracy display → check prediction charts → inspect GitHub repo contribution history.

### Use Cases

| ID | Use Case | Actor | Description | Priority |
| --- | --- | --- | --- | --- |
| `UC-01` | Domain-Filtered Discovery | Researcher | User selects "Computer Vision" filter → platform shows all CV papers/repos sorted by impact score | P0 |
| `UC-02` | LLM Insight Expansion | Researcher | User clicks on a paper card → expandable panel shows 3-sentence summary, 3 key takeaways, "why it matters" paragraph | P0 |
| `UC-03` | Trend Detection | Developer | User navigates to Trends view → sees which domains have spiked in activity over last 7–30 days | P1 |
| `UC-04` | Full-Text Search | Any | User types "diffusion models" in search → ranked results by relevance × impact score | P1 |
| `UC-05` | Repository Deep-Dive | Developer | User clicks repo card → sees stars, forks, predicted growth, last commit date, link to GitHub | P1 |
| `UC-06` | Paper Detail View | Researcher | User clicks paper card → sees authors, abstract, predicted citation growth, arXiv link | P1 |
| `UC-07` | Faculty Demo Navigation | Reviewer | Reviewer explores live platform, inspects classification tags, prediction gauges, and LLM summaries on any item | P0 |

---

PRD

## Feature Set

### F-01 · Data Feed & Ingestion Dashboard

- Auto-refreshed feed showing latest ingested items (papers, repos, articles) in a card grid
- Each card displays: title, source badge (arXiv / GitHub / HN), domain tags, impact score bar, and ingestion timestamp
- Feed sorted by impact score (default), recency, or domain activity (user-selectable)
- Infinite scroll or paginated navigation (20 items/page)
- Priority: P0

### F-02 · Domain Classification Display

- Each item tagged with 1 primary domain label + up to 2 secondary domain labels
- Domains: NLP, Computer Vision, Reinforcement Learning, IoT/Embedded, Systems/Infra, Robotics, Security, General ML, Data Engineering, Multimodal AI
- Left sidebar filter allows multi-select domain filtering; feed updates without full page reload
- Confidence score shown as a percentage on hover over domain tag
- Priority: P0

### F-03 · Impact Score Display

- Each item displays an "Impact Score" on a 0–10 scale with a horizontal color-coded bar (red→yellow→green)
- Score computed by the supervised ML prediction model (separate models for papers and repos)
- Tooltip on hover: lists the top 3 features that drove the score
- Rising indicator (animated badge) shown on items whose metrics spiked in last 48 hours
- Priority: P0

### F-04 · LLM-Generated Insight Cards

- Each item has an expandable "Insights" panel containing:
  - 3-sentence plain-English summary of the content
  - 3 key technical takeaways (bulleted)
  - 1 "Why this matters" paragraph contextualizing the broader impact
  - Technical depth indicator: Beginner / Intermediate / Advanced
  - Estimated read time in minutes
  - 3 related topic suggestions
- Panel shows a loading skeleton while LLM generation is pending
- Generated asynchronously on first expand; cached thereafter
- Priority: P0

### F-05 · Trend Analytics View

- Line chart: domain activity (item count per domain) over a rolling 7-day and 30-day window
- Bar chart: most active domains this week vs. last week (side-by-side comparison)
- Rising domains section: top 3 domains with steepest positive slope in activity
- All charts powered by Recharts; responsive down to mobile breakpoint
- Priority: P1

### F-06 · Full-Text Search

- Search bar in top nav accepts natural language queries
- Searches across: title, LLM-generated summary, domain tags, and metadata fields
- Results ranked by combined score: text relevance × impact score weight
- Domain filter applies to search results as well
- Priority: P1

### F-07 · Item Detail View

- **For GitHub repos:** current stars, forks, open issues, last commit date, primary language, topics, predicted 30-day star growth chart, link to GitHub
- **For arXiv papers:** full author list, submission date, abstract, predicted citation growth chart, link to arXiv page and PDF, link to associated code repo if detected
- **For HN articles:** original URL, upvote count, comment count, link to HN discussion
- All detail views include the full LLM insight card
- Priority: P1

### F-08 · Probation Contribution Visibility (Internal)

- Pragati Singh's GitHub commits are tagged under frontend components with clear scope prefixes
- POC (Sagnik) tracks weekly contribution count per member for Friday progress report
- All Pragati-assigned components (InsightPanel, TrendsPage, ItemCard) have clear ownership in GitHub CODEOWNERS
- Priority: P0 (internal requirement for lab evaluation)

PRD

## Non-Functional Requirements

| ID | Category | Requirement | Acceptance Criterion |
| --- | --- | --- | --- |
| `NFR-01` | Performance | Frontend page load | \< 2 seconds on a 4G connection (measured via Lighthouse) |
| `NFR-02` | Performance | API search response | \< 500ms at p95 latency (logged by FastAPI middleware) |
| `NFR-03` | Availability | Platform uptime during review | Live URL accessible and functional during all scheduled faculty review sessions |
| `NFR-04` | Accuracy | Classification accuracy | ≥ 85% top-1 accuracy, ≥ 0.80 macro F1 on 500-item test set |
| `NFR-05` | Accuracy | Prediction RMSE | ≤ 0.20 (on normalized 0–1 scale) via 5-fold cross-validation |
| `NFR-06` | Cost | LLM API spend | \< ₹500/month; achieved through caching + batching |
| `NFR-07` | Maintainability | Code documentation | All modules have docstrings; README with full local setup instructions |
| `NFR-08` | Traceability | GitHub contribution history | All 4 members have ≥ 10 commits each; no force pushes to main |
| `NFR-09` | Reliability | Ingestion failure handling | All ingestion tasks implement retry with exponential backoff; failures logged |
| `NFR-10` | Scalability | Data volume handling | Platform handles ≥ 10,000 items in DB without degrading feed performance |

PRD

## Feature Priority Matrix

| Feature | Priority | Complexity | Owner | Sprint |
| --- | --- | --- | --- | --- |
| Data Ingestion Pipeline (arXiv, GitHub, HN) | P0 | High | Udit | Sprint 1 |
| PostgreSQL schema + FastAPI skeleton | P0 | Medium | Shadwal | Sprint 1 |
| Domain Classification Model | P0 | High | Sagnik | Sprint 1–2 |
| Frontend: Feed + ItemCard + Domain Filter | P0 | Medium | Pragati + Shadwal | Sprint 1–2 |
| Impact Score ML Model (XGBoost) | P0 | High | Sagnik | Sprint 2 |
| LLM Insight Generation Pipeline | P0 | Medium | Sagnik | Sprint 2 |
| Feed API endpoints + DB joins | P0 | Medium | Shadwal | Sprint 2 |
| InsightPanel expandable component | P0 | Low | Pragati | Sprint 2 |
| Trend Analytics View + Charts | P1 | Medium | Pragati | Sprint 3 |
| Search endpoint + UI | P1 | Low | Shadwal | Sprint 3 |
| Item Detail Page | P1 | Low | Pragati + Shadwal | Sprint 3 |
| Domain trend aggregation task | P1 | Low | Udit | Sprint 3 |
| Deployment (Render + GitHub Actions CI/CD) | P0 | Medium | Shadwal | Sprint 4 |
| Historical data backfill (30-day trends) | P1 | Medium | Udit | Sprint 4 |
| Agent-based Q&A chat (ReAct) | P2 | High | Sagnik | Stretch |
| Weekly digest view | P2 | Medium | All | Stretch |

---

TRD

## System Architecture

ATIP is built as a three-tier web application with a decoupled async processing pipeline. The system separates the concerns of data ingestion, ML/LLM processing, storage, and presentation into distinct, independently scalable layers.

```
┌─────────────────────────────────────────────────────────────────────┐
│                         ATIP PLATFORM                               │
│                                                                     │
│  ┌───────────────────┐    ┌─────────────────┐    ┌───────────────┐  │
│  │   DATA SOURCES    │───▶│  INGESTION LAYER│───▶│  PROCESSING   │  │
│  │                   │    │                 │    │  PIPELINE     │  │
│  │  arXiv API        │    │  Celery Workers │    │               │  │
│  │  GitHub API v3    │    │  Redis Broker   │    │  Classifier   │  │
│  │  HN Algolia API   │    │  Celery Beat    │    │  (BART MNLI)  │  │
│  │  Semantic Scholar │    │  (Cron Sched.)  │    │  LLM Agent    │  │
│  │                   │    │                 │    │  XGBoost ML   │  │
│  └───────────────────┘    └─────────────────┘    └──────┬────────┘  │
│                                                         │           │
│  ┌──────────────────────────────────────────────────────▼────────┐  │
│  │                      STORAGE LAYER                            │  │
│  │    PostgreSQL 15 (Supabase)     Redis 7 (Upstash)             │  │
│  │    items · classifications      LLM output cache               │  │
│  │    insights · predictions       API response cache             │  │
│  │    domain_trends                                               │  │
│  └──────────────────────────────────┬─────────────────────────────┘  │
│                                     │                              │
│  ┌──────────────────────────────────▼─────────────────────────────┐  │
│  │                      BACKEND API                               │  │
│  │               FastAPI (Python 3.11) · Pydantic v2              │  │
│  │           /api/feed  /api/item  /api/trends  /api/search       │  │
│  └──────────────────────────────────┬─────────────────────────────┘  │
│                                     │                              │
│  ┌──────────────────────────────────▼─────────────────────────────┐  │
│  │                      FRONTEND                                  │  │
│  │         React 18 + Vite · TailwindCSS · Recharts               │  │
│  │         Zustand state · Axios HTTP · Lucide Icons               │  │
│  └────────────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────────┘
```

### Architecture Principles

- **Async-first processing:** All ingestion, classification, prediction, and LLM tasks run asynchronously via Celery so they never block the API or frontend
- **Cache aggressively:** LLM outputs are expensive and deterministic for a given input; they are cached in Redis indefinitely (invalidated only on model version bump)
- **Degrade gracefully:** If LLM insights aren't ready yet, the frontend shows a skeleton; the item card is still fully functional with classification and prediction data
- **Single deployable:** Backend + workers deployed as one unit on Render; frontend deployed separately as a static build on Vercel or Render's static hosting
- **Normalize at ingest:** All sources are normalized to a `RawItem` schema immediately on ingest, keeping downstream classification and prediction source-agnostic

TRD

## Data Ingestion Layer

### Source 1 — arXiv API

- **Endpoint:** `http://export.arxiv.org/api/query` (Atom/XML response, parsed with `feedparser`)
- **Categories fetched:** cs.LG (ML), cs.CV (Computer Vision), cs.CL (NLP), cs.RO (Robotics), cs.CR (Security), cs.SY (Systems), eess.SP (Signal Processing / IoT proxy)
- **Fields extracted:** paper_id, title, authors (list), abstract, categories, submitted_date, updated_date, PDF link
- **Schedule:** Daily at 00:30 IST via Celery Beat
- **Volume:** \~200 papers/day across these categories
- **Rate limiting:** 3 requests/second max; exponential backoff on 429 responses
- **Deduplication:** `ON CONFLICT (source_id) DO NOTHING` in PostgreSQL insert

### Source 2 — GitHub API v3

- **Endpoint:** `https://api.github.com/search/repositories`
- **Query strategy:** Search for `topic:machine-learning stars:>100 pushed:>[YESTERDAY]` and `topic:deep-learning`, rotating through ML-related topics daily
- **Fields extracted:** full_name, description, stargazers_count, forks_count, open_issues_count, pushed_at, topics, license.name, language, html_url
- **README enrichment:** Fetch `/repos/{owner}/{repo}/readme`, base64-decode, take first 600 characters for classification input
- **Schedule:** Daily at 01:00 IST
- **Auth:** GitHub Personal Access Token (PAT) stored in environment variable; 5000 req/hour authenticated limit
- **Volume:** \~150 repos/day filtered to quality threshold (≥100 stars, active in last 7 days)

### Source 3 — Hacker News Algolia API

- **Endpoint:** `https://hn.algolia.com/api/v1/search?tags=story&query=machine+learning&numericFilters=created_at_i>[UNIX_TS_6H_AGO]`
- **Queries rotated:** "machine learning", "LLM", "deep learning", "open source AI", "AI research"
- **Fields extracted:** objectID, title, url, points, num_comments, created_at, author
- **Schedule:** Every 6 hours (4 times/day)
- **No auth required**
- **Filter:** Only stories with points ≥ 20 and a valid external URL are ingested

### Source 4 — Semantic Scholar API (Enrichment)

- **Purpose:** Enrich arXiv papers with citation count, influential citation count, and author data for ML feature engineering
- **Endpoint:** `https://api.semanticscholar.org/graph/v1/paper/arXiv:{arxiv_id}`
- **Fields:** citationCount, influentialCitationCount, authors\[\].hIndex, year
- **Schedule:** Run once for each paper after ingestion; re-run weekly to update citation counts
- **Rate limit:** 100 req/5min unauthenticated; request API key for higher limits

### Unified RawItem Schema

```
class RawItem(BaseModel):
    source: str          # "arxiv" | "github" | "hn" | "semantic_scholar"
    source_id: str       # Original ID from source (e.g. "2410.12345")
    title: str
    description: str     # Abstract / README snippet / HN title
    url: str             # Canonical link to original resource
    metadata: dict       # Source-specific fields (stars, authors, etc.)
    ingested_at: datetime
    raw_content: str     # Full text used for classification
    created_at: Optional[datetime]  # Original publish/push date
```

### Ingestion Worker Architecture

- **Task queue:** Celery with Redis as the message broker
- **Scheduler:** Celery Beat with a crontab schedule defined in `celery_config.py`
- Each source has a dedicated Celery task; tasks are independent and failure-isolated
- On success: items are batch-inserted into the `items` table; a downstream `classify_new_items` task is chained via Celery Canvas
- On failure: task retries up to 3 times with 2^n minute backoff; failures are logged to a `pipeline_errors` table for monitoring

TRD

## Classification Layer

### Model Choice

**Primary:** `facebook/bart-large-mnli` (Zero-Shot Classification via HuggingFace Transformers). No labeled training data required. The model uses natural language inference to score each domain label against the item's content. Accuracy is strong out-of-the-box for technical domain classification.

**Fallback/Fast Path:** `distilbert-base-uncased` fine-tuned on arXiv CS category labels as a text classification head. 5× faster inference (\~200ms vs \~2.5s for BART). Used for high-volume batches when GPU is unavailable.

### Domain Taxonomy (v1)

```
DOMAIN_LABELS = [
    "Natural Language Processing",
    "Computer Vision",
    "Reinforcement Learning",
    "IoT and Embedded Systems",
    "Systems and Infrastructure",
    "Robotics",
    "Security and Privacy",
    "General Machine Learning",
    "Data Engineering and Pipelines",
    "Multimodal and Foundation Models"
]
```

### Classification Pipeline — Step by Step

1. **Input construction:** Concatenate `title + " . " + description[:600]` (truncated to avoid token limit overhead)
2. **Zero-shot inference:** Pass concatenated string + DOMAIN_LABELS to BART classifier via HuggingFace pipeline API
3. **Label assignment:**
   - Top-1 label = `primary_domain`
   - Labels ranked 2nd and 3rd where score > 0.15 = `secondary_domains[]`
   - All labels with score \< 0.05 are discarded
4. **Confidence check:** If max score \< 0.35, item is flagged as `low_confidence = true` and added to manual review queue
5. **Storage:** Insert row into `classifications` table; trigger next pipeline stage

### Batch Processing

- Process items in batches of 10 per Celery task invocation
- HuggingFace pipeline supports batch inference; pass list of 10 inputs per call
- On Google Colab (GPU): \~0.3s per item; on CPU: \~2.5s per item
- For demo-scale (\~500 items initial load), CPU batch processing completes in \~20 minutes

### Accuracy Evaluation Protocol

- **Test set:** 500 arXiv papers with known CS categories (cs.CL → NLP, cs.CV → CV, cs.RO → Robotics, etc.)
- **Mapping:** arXiv categories are deterministically mapped to DOMAIN_LABELS as ground truth
- **Metrics computed:** Top-1 accuracy, macro F1, per-domain precision and recall
- **Target:** ≥ 85% accuracy; if below threshold, switch to ensemble (BART + DistilBERT majority vote)
- **Logging:** Accuracy report written to `ml_reports/classification_eval_{date}.json` in repo

TRD

## LLM / Agent Intelligence Layer

### Model Selection

- **Primary:** `claude-sonnet-4-6` via Anthropic API — strong structured JSON output, accurate technical summarization
- **Budget fallback:** `gpt-4o-mini` via OpenAI API — significantly cheaper per token; used when monthly budget threshold is approached
- Model version stored in the `insights` table so outputs can be regenerated if model changes

### Insight Output Schema

```
{
  "summary": "3-sentence plain-English summary of the content",
  "key_takeaways": [
    "Technical takeaway 1",
    "Technical takeaway 2",
    "Technical takeaway 3"
  ],
  "why_it_matters": "1-paragraph significance statement",
  "technical_depth": "beginner | intermediate | advanced",
  "estimated_read_time_minutes": 12,
  "related_topics": ["topic1", "topic2", "topic3"]
}
```

### Prompt Template

```
SYSTEM:
You are a senior technical analyst specializing in machine learning and software engineering.
Your task is to generate a structured insight card for a piece of technical content.
Respond ONLY in valid JSON. No markdown, no preamble, no code fences.
Follow the schema exactly. All fields are required.

USER:
Title: {title}
Source Type: {source}   # arxiv | github | hn
Domain: {primary_domain}
Content:
{description[:1500]}

JSON Schema to follow:
{schema_json_string}
```

### Batching & Cost Management

- LLM tasks are grouped in batches of 20 items per Celery task invocation
- All outputs cached in Redis: key = `sha256(source_id + ":" + model_version)`, TTL = indefinite until model version bumps
- Before calling LLM API, always check Redis cache first; skip API call on cache hit
- JSON parsing errors trigger one automatic retry with a stricter prompt instruction
- Failed items (after 2 retries) are logged but do not block the pipeline; frontend shows "Insights unavailable" gracefully
- Budget monitoring: track token usage per day in a `llm_usage` table; alert (log warning) when daily spend exceeds ₹50

### Stretch — ReAct Agent (Sprint 4)

- A LangChain-powered ReAct agent with access to platform tools: `search_platform(query)`, `get_item_details(id)`, `compare_items(id1, id2)`, `get_domain_trends(domain, window)`
- Exposed via a chat UI component on the platform (floating chat bubble)
- Allows natural language queries: "What are the most impactful NLP papers from this week?" or "Compare this paper to the top Computer Vision repo"
- Agent conversation history maintained in session state (not persisted)

TRD

## ML Prediction Layer

### Prediction Tasks

Three separate supervised ML prediction tasks are defined, each targeting a different signal:

#### Task 1 — Paper Impact Score (Regression)

- **Target variable:** Normalized citation count at 6 months post-publication (from Semantic Scholar historical data). Normalized to 0–1 scale using log-transform + min-max normalization
- **Feature set:**
  - Author h-index (max h-index among all authors)
  - Author count (number of authors)
  - arXiv category (one-hot encoded; 7 categories)
  - Title word count
  - Abstract word count
  - Abstract Flesch-Kincaid readability score
  - Has GitHub link in abstract (binary)
  - Days since submission (at prediction time)
  - Classification confidence score
  - Number of figures (extracted from PDF metadata if available)
- **Model:** XGBoost Regressor (`n_estimators=300, max_depth=6, learning_rate=0.05`)

#### Task 2 — GitHub Repo Growth Score (Regression)

- **Target variable:** Stars gained in next 30 days (from historical repo snapshots captured daily). Normalized to 0–1
- **Feature set:**
  - Current star count (log-transformed)
  - Fork-to-star ratio
  - Open issues count
  - Days since last commit
  - README length (character count)
  - Number of topics/tags
  - License type (one-hot: MIT, Apache, GPL, none, other)
  - Primary language (one-hot: Python, JavaScript, Rust, Go, C++, other)
  - Classification confidence score
- **Model:** XGBoost Regressor (same hyperparams as Task 1) + Random Forest as baseline

#### Task 3 — Domain Trend Score (Classification)

- **Target variable:** Binary — is this domain "trending" this week? (defined as >20% week-over-week increase in item count)
- **Features:** 7-day rolling item count per domain, 7-day rolling average impact score per domain, week-over-week delta
- **Model:** Logistic Regression (simple, interpretable; sufficient for this binary task)

### Feature Engineering Pipeline

```
class FeatureExtractor:
    def extract_arxiv_features(self, item: RawItem) -> dict:
        return {
            "title_word_count": len(item.title.split()),
            "abstract_word_count": len(item.description.split()),
            "flesch_score": textstat.flesch_reading_ease(item.description),
            "domain_confidence": item.classification_score,
            "author_count": len(item.metadata.get("authors", [])),
            "max_author_hindex": item.metadata.get("max_h_index", 0),
            "days_since_submission": (datetime.now() - item.created_at).days,
            "has_code_link": int("github" in item.description.lower()),
        }

    def extract_github_features(self, item: RawItem) -> dict:
        m = item.metadata
        stars = max(m.get("stargazers_count", 1), 1)
        return {
            "stars_log": math.log1p(stars),
            "forks": m.get("forks_count", 0),
            "fork_star_ratio": m.get("forks_count", 0) / stars,
            "open_issues": m.get("open_issues_count", 0),
            "readme_length": len(m.get("readme_snippet", "")),
            "topic_count": len(m.get("topics", [])),
            "days_since_commit": compute_days_since(m.get("pushed_at")),
            "domain_confidence": item.classification_score,
        }
```

### Training & Evaluation

- **Dataset construction:** Historical data collected starting Day 1 of the project. arXiv papers enriched with Semantic Scholar citations (6-month lag needed; use pre-2026 papers for training set). GitHub repos: snapshot star counts daily; label = stars gained in 30 days
- **Train/test split:** 80/20 stratified by source and domain
- **Cross-validation:** 5-fold CV; report mean and std of RMSE and R²
- **Model artifacts:** Saved as `.pkl` files via `joblib`; stored in `models/` directory in repo
- **Retraining schedule:** Retrain weekly as more data accumulates (triggered by Celery Beat)

**Data Cold-Start Note** The team should start collecting GitHub repo snapshots and tracking citation counts from Day 1. Without historical data accumulation, the ML models can only be trained on pre-existing open datasets (e.g., Semantic Scholar Open Research Corpus). Synthetic augmentation via feature perturbation is an acceptable fallback for demo purposes but must be disclosed.

TRD

## Frontend Layer

### Page Routes

| Route | Page | Description |
| --- | --- | --- |
| `/` | Dashboard | Main feed with domain filter sidebar, sort controls, trending banner |
| `/trends` | Trend Analytics | Domain activity line chart, bar chart, rising domains list |
| `/explore/:domain` | Domain Explorer | Deep-dive into a single domain; all items + domain-specific trend |
| `/item/:id` | Item Detail | Full insight card, prediction widget, metadata table, source link |
| `/search` | Search Results | Full-text search results with domain and sort filters |

### Component Architecture

App ├── Layout │ ├── Sidebar (domain filter checkboxes, navigation links) │ └── TopBar (search input, sort dropdown, date range picker) ├── /dashboard → Dashboard │ ├── TrendingBanner (top 3 rising items, auto-rotated) │ ├── FeedList │ │ └── ItemCard (×N) │ │ ├── SourceBadge (arXiv / GitHub / HN) │ │ ├── DomainTag\[\] (primary + secondary) │ │ ├── ImpactScoreBar (colored 0–10 bar) │ │ ├── RisingBadge (conditional, if trend spike) │ │ └── InsightPanel (expandable, lazy-loaded) │ │ ├── SummaryText │ │ ├── KeyTakeawayList │ │ ├── WhyItMatters │ │ └── TechnicalDepthTag │ └── DomainSummaryRow (quick counts per domain) ├── /trends → TrendsPage │ ├── DomainActivityLineChart (Recharts LineChart) │ ├── WeeklyComparisonBarChart (Recharts BarChart) │ └── RisingDomainsList ├── /item/:id → ItemDetailPage │ ├── FullInsightCard │ ├── PredictionWidget │ │ ├── ScoreGauge (custom SVG arc gauge) │ │ └── GrowthProjectionChart (Recharts AreaChart) │ └── MetadataTable (source-specific key-value pairs) └── /search → SearchPage ├── SearchResultsList └── ItemCard (same component, search-result variant)

### State Management (Zustand)

```
const useFeedStore = create((set) => ({
  items: [],
  selectedDomains: [],        // multi-select domain filter
  sortBy: "impact_score",     // "impact_score" | "recent" | "trending"
  page: 1,
  isLoading: false,
  setItems: (items) => set({ items }),
  toggleDomain: (domain) => set((state) => ({
    selectedDomains: state.selectedDomains.includes(domain)
      ? state.selectedDomains.filter(d => d !== domain)
      : [...state.selectedDomains, domain]
  })),
  setSortBy: (sort) => set({ sortBy: sort, page: 1 }),
}));
```

### API Integration

| Component | API Call | Caching |
| --- | --- | --- |
| FeedList | `GET /api/feed?domain=&sort=&page=` | React Query; stale-while-revalidate 5 min |
| InsightPanel | `GET /api/item/{id}/insights` | React Query; cache indefinitely (insights don't change) |
| TrendsPage | `GET /api/trends?window=7d` | React Query; stale after 1 hour |
| ItemDetailPage | `GET /api/item/{id}` | React Query; stale after 30 min |
| SearchPage | `GET /api/search?q=&domain=` | No cache (query-dependent) |

TRD

## Database Schema & API Design

### PostgreSQL Tables

#### items

```
CREATE TABLE items (
    id           UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    source       VARCHAR(50)  NOT NULL,     -- "arxiv" | "github" | "hn"
    source_id    VARCHAR(200) UNIQUE NOT NULL, -- original ID
    title        TEXT         NOT NULL,
    description  TEXT,
    url          TEXT         NOT NULL,
    metadata     JSONB,                       -- source-specific fields
    ingested_at  TIMESTAMPTZ  DEFAULT NOW(),
    created_at   TIMESTAMPTZ                  -- original publish date
);
CREATE INDEX idx_items_source ON items(source);
CREATE INDEX idx_items_ingested ON items(ingested_at DESC);
```

#### classifications

```
CREATE TABLE classifications (
    id                UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    item_id           UUID REFERENCES items(id) ON DELETE CASCADE,
    primary_domain    VARCHAR(100),
    secondary_domains TEXT[],
    confidence_scores JSONB,      -- {"NLP": 0.82, "CV": 0.11, ...}
    low_confidence    BOOLEAN DEFAULT FALSE,
    model_version     VARCHAR(50),
    classified_at     TIMESTAMPTZ DEFAULT NOW()
);
CREATE INDEX idx_cls_domain ON classifications(primary_domain);
CREATE INDEX idx_cls_item_id ON classifications(item_id);
```

#### insights

```
CREATE TABLE insights (
    id                   UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    item_id              UUID REFERENCES items(id) ON DELETE CASCADE,
    summary              TEXT,
    key_takeaways        TEXT[],
    why_it_matters       TEXT,
    technical_depth      VARCHAR(20),    -- "beginner"|"intermediate"|"advanced"
    estimated_read_time  INT,
    related_topics       TEXT[],
    llm_model            VARCHAR(100),
    generated_at         TIMESTAMPTZ DEFAULT NOW()
);
```

#### predictions

```
CREATE TABLE predictions (
    id               UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    item_id          UUID REFERENCES items(id) ON DELETE CASCADE,
    prediction_type  VARCHAR(50),  -- "impact_score"|"growth_score"
    score            FLOAT,         -- 0.0 to 1.0 (normalized)
    score_display    FLOAT,         -- 0.0 to 10.0 (for UI)
    confidence       FLOAT,
    features_used    JSONB,
    model_version    VARCHAR(50),
    predicted_at     TIMESTAMPTZ DEFAULT NOW()
);
CREATE INDEX idx_pred_item ON predictions(item_id);
CREATE INDEX idx_pred_score ON predictions(score DESC);
```

#### domain_trends

```
CREATE TABLE domain_trends (
    id            UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    domain        VARCHAR(100),
    date          DATE,
    item_count    INT,
    avg_impact    FLOAT,
    trend_score   FLOAT,   -- slope of 7-day rolling count
    is_trending   BOOLEAN DEFAULT FALSE,
    UNIQUE(domain, date)
);
```

### FastAPI Endpoint Specifications

| Method | Endpoint | Query Params | Response |
| --- | --- | --- | --- |
| `GET` | `/api/feed` | `domain, sort, page, limit` | Paginated list of items with classification + prediction joined |
| `GET` | `/api/item/{id}` | — | Full item with metadata, classification, prediction, insights |
| `GET` | `/api/item/{id}/insights` | — | Insight card; triggers LLM generation if not yet cached |
| `GET` | `/api/trends` | `window (7d\|30d), domain` | Domain trend time-series + trend scores |
| `GET` | `/api/search` | `q, domain, sort, page` | Ranked search results (PostgreSQL full-text search + score reranking) |
| `GET` | `/api/domains` | — | List of all domain labels with item counts and trend status |
| `GET` | `/api/health` | — | System health: DB ping, Redis ping, last ingestion timestamp |
| `POST` | `/api/admin/refresh` | Bearer token required | Manually trigger full ingestion cycle |

---

Workflow

## End-to-End Data Flow

The ATIP processing pipeline runs on a fully automated schedule. The following describes the complete journey from raw external API data to a rendered insight card in the user interface.

STEP 1: INGESTION \[Daily, 00:30–01:30 IST via Celery Beat\] ├──▶ fetch_arxiv_papers() → 200 papers from cs.LG / cs.CL / cs.CV ... ├──▶ fetch_github_repos() → 150 repos (stars ≥ 100, pushed \< 24h ago) ├──▶ fetch_hn_stories() → 50 stories (points ≥ 20, ML-related) └──▶ normalize_to_raw_item() → Unified RawItem schema for all sources → INSERT INTO items ON CONFLICT DO NOTHING → Net new items emitted to queue for Step 2 STEP 2: ENRICHMENT \[Runs after ingestion, for arXiv items only\] └──▶ enrich_with_semantic_scholar() ├──▶ For each new arXiv paper: GET /paper/arXiv:{id} └──▶ UPDATE items.metadata with citationCount + author h-index STEP 3: CLASSIFICATION \[Runs after Step 1 completes\] └──▶ classify_new_items() → Fetch all items WHERE classification IS NULL ├──▶ Batch 10 items → BART zero-shot classifier ├──▶ Assign primary_domain + secondary_domains + confidence_scores ├──▶ INSERT INTO classifications └──▶ Flag low_confidence items (score \< 0.35) → review queue STEP 4: FEATURE EXTRACTION & PREDICTION \[Runs after Step 3\] └──▶ predict_new_items() → Fetch all classified items WHERE prediction IS NULL ├──▶ FeatureExtractor.extract(item) → feature dict ├──▶ XGBoost model inference → score (0.0–1.0) ├──▶ Scale to display score (0.0–10.0) └──▶ INSERT INTO predictions STEP 5: LLM INSIGHT GENERATION \[Runs concurrently with Step 4\] └──▶ generate_insights() → Fetch classified items WHERE insight IS NULL ├──▶ Check Redis cache (sha256 key) → skip if hit ├──▶ Build prompt from template → call LLM API (batch 20 items) ├──▶ Parse JSON response → validate schema ├──▶ INSERT INTO insights └──▶ SET Redis cache (indefinite TTL) STEP 6: DOMAIN TREND AGGREGATION \[Daily, after Steps 3–5\] └──▶ aggregate_domain_trends() ├──▶ COUNT items per domain for today ├──▶ AVG(prediction.score) per domain for today ├──▶ Compute trend_score = slope(7-day rolling count) ├──▶ Flag is_trending = TRUE if WoW increase > 20% └──▶ INSERT INTO domain_trends ON CONFLICT (domain, date) DO UPDATE ✓ PIPELINE COMPLETE → All new items are classified, scored, and insight-ready

### Error Handling & Recovery

- Each Celery task has `max_retries=3` and `countdown=2**retries * 60` seconds
- Permanent failures are written to a `pipeline_errors` table with error message, task name, and item_id
- A `/api/health` endpoint exposes last successful run timestamps for each pipeline stage
- If LLM API is down, insight generation is skipped and items remain available with classification and prediction data visible in the UI
- If classification fails for an item, the item still appears in the feed under "Unclassified" with a warning tag

Workflow

## User Request Flow

### Dashboard Load Flow

USER opens browser → http://atip.yourdomain.com ① React app loads (Vite build served as static files from CDN/Render) ② Zustand store initializes: selectedDomains = \[\], sortBy = "impact_score", page = 1 ③ FeedList mounts → Axios GET /api/feed?sort=impact_score&page=1&limit=20 └──▶ FastAPI receives request ├──▶ Check Redis cache for this query key → miss on first load ├──▶ Query PostgreSQL: │ SELECT i.\*, c.primary_domain, c.secondary_domains, │ p.score_display, p.confidence, ins.summary │ FROM items i │ LEFT JOIN classifications c ON i.id = c.item_id │ LEFT JOIN predictions p ON i.id = p.item_id │ AND p.prediction_type = 'impact_score' │ LEFT JOIN insights ins ON i.id = ins.item_id │ ORDER BY p.score_display DESC NULLS LAST │ LIMIT 20 OFFSET 0 ├──▶ Serialize to FeedResponse JSON └──▶ Cache in Redis (key: feed:impact_score:p1:all, TTL: 5min) ④ React renders 20 ItemCard components ├──▶ SourceBadge, DomainTag\[\], ImpactScoreBar visible immediately └──▶ InsightPanel collapsed (lazy: no API call yet) ✓ Dashboard fully rendered in \< 2 seconds

### Insight Panel Expand Flow

USER clicks on ItemCard to expand InsightPanel ① InsightPanel state: collapsed → expanded ② React Query checks cache for GET /api/item/{id}/insights → miss ③ Skeleton loader shown immediately (UX: no blank state) ④ Axios GET /api/item/{id}/insights └──▶ FastAPI checks insights table for item_id ├──▶ \[HIT\] Return stored insight JSON → \~20ms response └──▶ \[MISS\] Trigger generate_insight.delay(item_id) as async Celery task └──▶ Return 202 Accepted + task_id ⑤ \[If 202\] Frontend polls GET /api/insights/status/{task_id} every 3s ⑥ When task completes, frontend refetches /api/item/{id}/insights ⑦ InsightPanel renders: summary, key_takeaways, why_it_matters, depth tag ✓ Insight visible within 5–10 seconds on first expand; instant on subsequent

### Search Flow

USER types "transformer architecture" in search bar → presses Enter ① Navigate to /search?q=transformer+architecture ② Axios GET /api/search?q=transformer+architecture&page=1 └──▶ FastAPI: ├──▶ PostgreSQL full-text search: │ SELECT i.\*, ts_rank(to_tsvector(title || ' ' || description), │ plainto_tsquery('transformer architecture')) as text_rank, │ p.score_display as impact_score │ WHERE to_tsvector(...) @@ plainto_tsquery(...) │ ORDER BY (text_rank * 0.4 + p.score_display * 0.6) DESC └──▶ Return ranked SearchResponse ③ SearchPage renders result cards (same ItemCard component) ④ User applies domain filter → re-queries with domain param ✓ Search results visible within 500ms

---

Tech

## Tech Stack

### Backend

| Component | Technology | Version | Rationale |
| --- | --- | --- | --- |
| API Framework | FastAPI | 0.111+ | Async support, auto OpenAPI docs, Pydantic v2 validation |
| Task Queue | Celery + Redis | 5.x + 7.x | Reliable async task execution, cron scheduling via Beat |
| Database | PostgreSQL 15 | 15 | JSONB for flexible metadata, full-text search, ACID compliance |
| Cache | Redis 7 | 7 | LLM output caching, API response caching, task broker |
| ML Runtime | scikit-learn + XGBoost | 1.5 + 2.x | Standard, well-documented, CPU-deployable |
| Classification | HuggingFace Transformers (BART) | 4.x | Zero-shot; no labeled training data needed |
| LLM Client | Anthropic Python SDK | 0.30+ | Structured output, reliable JSON generation |
| Text Features | textstat + spaCy | — | Readability scoring, NLP feature extraction |
| HTTP Clients | httpx (async) | 0.27+ | Async-native; better than requests for FastAPI apps |
| Python Version | Python 3.11 | 3.11 | Best performance; required for latest library compat |

### Frontend

| Component | Technology | Rationale |
| --- | --- | --- |
| Framework | React 18 + Vite | Fast HMR dev builds, tree-shaking, excellent DX |
| Styling | TailwindCSS 3 | Utility-first; rapid iteration without custom CSS sprawl |
| Charts | Recharts | Declarative, React-native; excellent for time-series and bar charts |
| State | Zustand | Minimal boilerplate; no Redux overhead for this scope |
| Data Fetching | TanStack Query (React Query) | Caching, stale-while-revalidate, background refetch |
| HTTP | Axios | Interceptors, error handling, request/response transform |
| Icons | Lucide React | Consistent, lightweight icon set |
| Routing | React Router v6 | Standard; declarative route config |

### Infrastructure

| Component | Service | Tier / Cost | Notes |
| --- | --- | --- | --- |
| Backend hosting | Render.com | Free (or Starter $7/mo) | Supports Python + background workers |
| Frontend hosting | Vercel | Free | Static build; global CDN edge delivery |
| Database | Supabase (PostgreSQL) | Free (500MB, 2 projects) | Managed PG; includes connection pooling via PgBouncer |
| Redis | Upstash Redis | Free (10,000 req/day) | Serverless Redis; no persistent connection needed |
| Model storage | GitHub LFS | Free (1GB) | Store trained .pkl model artifacts in repo |
| CI/CD | GitHub Actions | Free (public repo) | Run tests + deploy on push to main |
| ML compute | Google Colab (GPU) | Free | For BART inference batch runs and model training |

Execution

## Team & Sprint Plan

### Team Members

Sagnik Pramanik

24052102 · 3rd Year

Project POC · ML Lead

Domain classification model, XGBoost prediction models, LLM insight pipeline, weekly Friday progress reports to leadership board

Shadwal Singh

25051314

Full-Stack · Infra

FastAPI backend, PostgreSQL schema design, Redis integration, deployment pipeline (Render + GitHub Actions), search endpoint

Udit Kumar Jaiswal

25156129

Data Engineering · ML Ops

Celery ingestion workers (arXiv, GitHub, HN), Semantic Scholar enrichment, feature extraction pipeline, domain trend aggregation

Pragati Singh

25051640 · Probation

Frontend

React components: ItemCard, InsightPanel, TrendsPage, DomainFilter sidebar, responsive layout. Clear GitHub commit history required for probation evaluation

### Lab Attendance

| Member | Mon | Tue | Wed | Thu | Fri | Sat |
| --- | --- | --- | --- | --- | --- | --- |
| Sagnik | ✓ |  |  | ✓ | ✓ |  |
| Shadwal | ✓ | ✓ |  |  | ✓ | ✓ |
| Udit |  | ✓ | ✓ |  |  | ✓ |
| Pragati |  |  |  | ✓ | ✓ | + 1 TBD with POC |

**Overlap days for in-person syncs:** Monday (Sagnik + Shadwal), Friday (Sagnik + Shadwal + Pragati). Weekly review submitted by Sagnik every Friday evening to Hitesh, Naman, and Ritisha.

### Sprint Plan

Sprint 1 — Foundation Week 1

- **Shadwal:** Initialize GitHub repo with monorepo structure (backend/ + frontend/). Set up FastAPI skeleton with health endpoint. Define PostgreSQL schema, connect to Supabase, run migrations. Set up Redis (Upstash). Write .env.example with all required keys.
- **Udit:** Implement arXiv ingestion Celery task. Implement GitHub ingestion Celery task. Set up Celery Beat schedule. Normalize all items to RawItem schema. Verify items appear in DB.
- **Sagnik:** Implement BART MNLI zero-shot classifier. Test on 500 arXiv paper sample. Generate accuracy report. Write classification Celery task. Confirm pipeline: ingest → classify → DB.
- **Pragati:** Initialize React + Vite + TailwindCSS project. Build ItemCard component (static props). Build DomainTag and SourceBadge components. Build layout with sidebar placeholder.

**Deliverable:** Raw items flowing into DB; classifier running locally with accuracy report; static frontend layout

Sprint 2 — Core ML + LLM + API Week 2

- **Sagnik:** Build XGBoost feature pipeline and train impact score model (Task 1 + Task 2). Implement LLM insight generation Celery task. Prompt engineering + JSON parsing. Redis caching for LLM outputs.
- **Udit:** Add HN ingestion task. Add Semantic Scholar enrichment task. Build FeatureExtractor class for both source types. Integrate with prediction pipeline.
- **Shadwal:** Build /api/feed endpoint with JOIN query. Build /api/item/{id} and /api/item/{id}/insights endpoints. Add Redis caching for feed responses. Add Axios config in frontend.
- **Pragati:** Connect FeedList to /api/feed (Axios + React Query). Make ItemCard data-driven. Build ImpactScoreBar component. Build DomainFilter sidebar (Zustand state). Build InsightPanel (expandable, skeleton loader).

**Deliverable:** Full pipeline working: ingest → classify → predict → insights → API → UI feed visible in browser

Sprint 3 — Trends + Search + Polish Week 3

- **Sagnik:** Fine-tune LLM prompts based on output quality review. Train domain trend logistic regression model (Task 3). Write classification accuracy docs for README.
- **Udit:** Build domain_trends aggregation Celery task. Backfill 7 days of trend data. Build /api/trends endpoint in coordination with Shadwal.
- **Shadwal:** Build /api/search endpoint (PostgreSQL full-text + score reranking). Build /api/trends and /api/domains endpoints. Pagination on all list endpoints. Response time monitoring middleware.
- **Pragati:** Build TrendsPage with DomainActivityLineChart (Recharts) and WeeklyComparisonBarChart. Build SearchPage with SearchResultsList. Build ItemDetailPage (/item/:id). Responsive design across all pages.

**Deliverable:** All P1 features working; trends charts visible; search functional; item detail page complete

Sprint 4 — Deployment + Demo Prep Week 4

- **Shadwal:** Deploy backend to Render (web service + worker process). Deploy frontend to Vercel. Set up GitHub Actions CI/CD (test → lint → deploy on push to main). Write full README with setup instructions, architecture diagram, API docs link.
- **Udit:** Backfill 30 days of domain trend data for charts. Set up daily GitHub repo snapshot collection for growth prediction training data. Monitor ingestion pipeline for 48 hours post-deployment.
- **Sagnik:** Prepare Friday progress report for leadership board. Document ML model accuracy metrics. Finalize model artifacts in repo. Prepare demo script (5-min walkthrough of key features).
- **Pragati:** Final responsive design pass (mobile + tablet). Fix any visual bugs from cross-browser testing. Ensure all frontend components have clear prop types and JSDoc. Accessibility pass (keyboard nav, contrast ratios).

**Deliverable:** Live public URL. GitHub repo with full contribution history. Faculty-ready demo. All NFRs met.

### GitHub Conventions

- **Branch naming:** `feature/[name]-[feature]` e.g. `feature/pragati-insight-panel`, `feature/udit-arxiv-ingestion`
- **Commit format:** `[scope]: description` e.g. `[ml]: add xgboost impact predictor`, `[frontend]: build insight panel component`, `[api]: add search endpoint with reranking`
- **PR policy:** Sagnik reviews and merges all PRs to `main`. No direct pushes to main.
- **CODEOWNERS file:** Maps `frontend/src/components/InsightPanel` and `frontend/src/pages/TrendsPage` to @pragati for clear contribution attribution
- **Weekly Friday:** Sagnik submits progress update to Hitesh, Naman, and Ritisha covering: tasks completed, tasks pending, blockers, attendance log

Risks

## Risk Register & Assumptions

| ID | Risk | Likelihood | Impact | Mitigation | Owner |
| --- | --- | --- | --- | --- | --- |
| `R-01` | Insufficient historical data for ML model training (cold-start problem) | High | High | Start collecting GitHub snapshots + arXiv enrichment from Day 1. Use Semantic Scholar Open Research Corpus (pre-2024 papers) as supplemental training data. Disclose synthetic augmentation if used. | Udit, Sagnik |
| `R-02` | BART classifier accuracy below 85% target | Medium | Medium | Implement ensemble: majority vote between BART MNLI + fine-tuned DistilBERT. If still below target, use arXiv category labels directly as ground truth for fine-tuning. | Sagnik |
| `R-03` | LLM API costs exceed lab budget | Medium | Medium | Redis caching eliminates repeat calls. Use gpt-4o-mini as cost fallback. Process only P0 items with full LLM pass; HN items get lighter summarization. | Sagnik, Shadwal |
| `R-04` | Platform inaccessible during faculty review | Medium | Critical | Deploy to Render in Sprint 1 (not Sprint 4). Maintain a local demo fallback (Docker Compose + ngrok) that can run from a laptop in 5 minutes. Test URL 48h before every review. | Shadwal |
| `R-05` | GitHub / arXiv API rate limits causing ingestion failures | Medium | Medium | Exponential backoff on all external API calls. GitHub PAT authenticated requests (5000/hr vs 60/hr unauthenticated). Spread scheduled calls across different hours. | Udit |
| `R-06` | Pragati's contributions insufficient for probation evaluation | Medium | High | POC assigns specific, scoped components with clear GitHub ownership (CODEOWNERS). Weekly check-in between Sagnik and Pragati on Thu/Fri. Tasks escalated to leadership board early if contribution is at risk. | Sagnik |
| `R-07` | Team availability conflicts due to lab day mismatch | Low | Low | Async collaboration via GitHub PR comments and shared Notion/docs. Sync sessions on Mon (Sagnik + Shadwal) and Fri (all who overlap). Udit syncs with Sagnik on Tue. | All |
| `R-08` | BART inference too slow for batch processing without GPU | Medium | Low | Use Google Colab for batch classification runs. DistilBERT fallback on CPU (\~200ms/item). For demo, ensure all displayed items are pre-classified. | Sagnik |

### Assumptions

- Anthropic API access (or OpenAI API as fallback) is available to the team for LLM insight generation
- Free-tier hosting on Render, Supabase, and Upstash is sufficient for demo-scale traffic (single faculty review session)
- arXiv, GitHub v3, and HN Algolia APIs remain publicly accessible throughout the 4-week build window
- A Google Colab session with GPU access is available for BART batch classification and XGBoost model training
- Semantic Scholar API free tier (100 req/5min) is sufficient; escalation to API key request if more volume needed
- The team treats this PRD as a living document; Sagnik (POC) has authority to revise scope, feature prioritization, and model choices during sprint planning without re-approval

[↑ back to top](#cover)