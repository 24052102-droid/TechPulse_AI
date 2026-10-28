# TechPulse AI (ATIP)

**Autonomous Technical Intelligence & Prediction Platform**  
*Built at IoT Lab — Machine Learning · Campus 25, KIIT University*

---

## What is this?

Keeping up with technical papers, open-source releases, and tech discussions is noisy. Most developers and researchers drown in arXiv uploads, GitHub trends, and Hacker News threads without knowing what actually matters or where developer adoption is really heading.

**TechPulse AI (ATIP)** solves this by running an autonomous 6-stage intelligence pipeline. It continuously pulls fresh content from arXiv, GitHub, and Hacker News, maps every item into a 10-domain taxonomy, scores its predicted 6-month impact using trained gradient boosting models (with TreeSHAP explainability for every score), generates structured AI synthesis cards, and tracks macro domain trends on an interactive Technology Radar.

Everything runs locally out of the box with zero external infrastructure required (SQLite + in-memory cache fallbacks are built in), or plugs straight into Supabase PostgreSQL and Upstash Redis for production.

---

## Quickstart (Up & Running in 2 Minutes)

You need **Python 3.10+** and **Node.js 18+**.

### 1. Grab the repository & set up Python

```bash
git clone https://github.com/shadwalsr/TechPulse-AI.git
cd TechPulse-AI

# Create and activate virtual environment
python -m venv venv
# Windows:
venv\Scripts\activate
# Linux / macOS:
source venv/bin/activate

# Install backend dependencies
pip install -r backend/requirements.txt
```

*(If you don't have a `requirements.txt` handy, install: `fastapi uvicorn sqlalchemy xgboost scikit-learn textstat joblib pandas numpy httpx requests pydantic-settings`)*

### 2. Configure Environment

Copy the template:
```bash
cp .env.example .env
```
By default, `.env` points to local SQLite (`sqlite:///./techpulse.db`) and in-memory caching. You can run the entire platform immediately without signing up for any cloud services.

### 3. Start the Backend

```bash
python -m uvicorn backend.app.main:app --port 8000 --reload
```
The FastAPI server will boot at **http://127.0.0.1:8000**.  
Interactive OpenAPI documentation is live at **http://127.0.0.1:8000/docs**.

### 4. Start the Frontend

In a separate terminal:
```bash
cd Frontend
npm install
npm run dev
```
Open your browser to **http://localhost:5173** to see the feed, trends radar, and evaluation scorecards.

---

## How It Works (The 6-Stage Pipeline)

Instead of relying on LLMs for everything (which gets slow and expensive), ATIP uses a layered architecture where fast, deterministic ML does the heavy lifting, and LLMs are called only for structured synthesis.

```
[ arXiv / GitHub / HN ]
         │
         ▼
[ Stage 1: Ingestion ] ────── Deduplication on source_id, rate-limited polling
         │
         ▼
[ Stage 2: Enrichment ] ───── Semantic Scholar author h-index & repo link regex
         │
         ▼
[ Stage 3: Classification ] ── 10-domain zero-shot taxonomy + confidence scoring
         │
         ├────────────────────────────────────────┐
         ▼                                        ▼
[ Stage 4: XGBoost Prediction ]          [ Stage 5: LLM Synthesis ]
  • Paper Impact Model (RMSE: 0.096)       • Claude / GPT synthesis
  • Repo Growth Model  (RMSE: 0.062)       • Strict JSON schema output
  • TreeSHAP top 3 feature drivers         • Redis cache-first guardrail
         │                                        │
         └───────────────────┬────────────────────┘
                             ▼
[ Stage 6: Trends & Radar Aggregation ]
  • 7-day rolling linear regression slopes
  • Week-over-week velocity & Hype-vs-Adoption matrix
```

1. **Autonomous Ingestion (`tasks/ingest.py`):** Pulls from arXiv API (`cs.LG`, `cs.CV`, `cs.CL`, `cs.RO`, `cs.CR`, `cs.SY`, `eess.SP`), GitHub Search API (`stars:>100`, pushed recently, active topics), and Hacker News Algolia API. Net-new items are upserted idempotently.
2. **Academic & Repo Enrichment (`tasks/enrich.py`):** Automatically hits Semantic Scholar to fetch author $h$-index and historical citations for papers, and extracts repo links from abstracts.
3. **10-Domain Classification (`tasks/classify.py`):** Assigns primary domain, secondary categories, and calibrated confidence scores across our technical taxonomy (NLP, Computer Vision, Reinforcement Learning, Robotics, Security, Systems, Data Engineering, IoT, Multimodal, General ML).
4. **Supervised Impact Prediction (`tasks/predict.py`):** Pretrained XGBoost regressors score each item on a 0.0 to 10.0 scale. Alongside the raw score, it runs exact TreeSHAP (`pred_contribs=True`) to save the top 3 positive/negative feature drivers so every prediction is explainable.
5. **AI Synthesis Cards (`tasks/insights.py`):** Produces high-signal 3-sentence summaries, 3 key takeaways, technical depth tag, estimated read time, and "why it matters" notes. Every insight is cached by SHA-256 hash so we never pay for the same item twice.
6. **Technology Radar & Trend Analysis (`tasks/trends.py`):** Aggregates daily domain statistics, calculates 7-day regression momentum, flags week-over-week surges, and computes the Hype vs. Adoption ratio (paper count vs. repo count).

---

## The ML Models (And How We Solved Cold Start)

A core challenge with predictive tech scoring is the **Cold-Start Problem**: you can't train a model to predict 6-month paper citations or 30-day GitHub star velocity using fresh Day-1 data because the future hasn't happened yet.

### 1. Retrospective Historical Datasets
- **arXiv Impact Dataset ($N = 1,118$ papers):** Collected papers submitted 7 to 18 months ago, extracted submission-date metadata ($t_0$), and measured observed citations at $t_0 + 180\text{d}$ via Semantic Scholar. Target: $y_{\text{paper}} = \text{normalized}(\ln(1 + \text{citations}_{180\text{d}}))$.
- **GitHub Velocity Dataset ($N = 8,679$ repos):** Reconstructed star velocity over 30-day windows. Target: $y_{\text{repo}} = \text{normalized}(\ln(1 + \Delta S_{30\text{d}}))$.

### 2. Time-Based Splitting (No Random Shuffle)
To avoid lookahead bias and data leakage, data was split strictly **chronologically**: the oldest 80% was used for training / 5-fold cross-validation, and the most recent 20% was held out as the test set.

### 3. Model Benchmark Results

| Model Task | Baseline (Ridge Regression) | Random Forest | **XGBoost (Selected)** | Target Met |
| :--- | :--- | :--- | :--- | :---: |
| **Paper Impact (180d Citations)** | 5-Fold CV RMSE: 0.1117<br>Holdout RMSE: 0.1919 | CV RMSE: 0.0879<br>Holdout RMSE: 0.1298 | **CV RMSE: 0.0959 (±0.010)**<br>**Holdout RMSE: 0.1348 (R²: 0.527)** | ✅ (Target $\le 0.20$) |
| **Repo Growth (30d Star Velocity)** | 5-Fold CV RMSE: 0.1010<br>Holdout RMSE: 0.0516 | CV RMSE: 0.0637<br>Holdout RMSE: 0.0360 | **CV RMSE: 0.0617 (±0.002)**<br>**Holdout RMSE: 0.0359 (R²: 0.526)** | ✅ (Target $\le 0.20$) |
| **Domain Trend Classifier** | — | — | **Accuracy: 74.2%** | ✅ |

### 4. What Features Actually Drive Predictions?
- **For research papers:** `max_author_hindex` (33.1% weight), primary category (`cs.LG`, `cs.CV`), presence of an open-source code repository link in abstract (+8.1%), and Flesch readability.
- **For repositories:** `days_since_commit` (recency of activity: 28.4%), log of current stars (19.6%), fork-to-star ratio, and primary language.

Full decision tree representations of the trained models are exported in [`model_decision_trees/`](model_decision_trees/).

---

## Exploring the Frontend

The frontend is built with React 18, Vite, TailwindCSS, Zustand, and Lucide icons.

- **`/` — Intelligence Feed:** Browse classified technical cards with instant domain pills, source badges, impact score bars with hover tooltips showing TreeSHAP drivers, and expandable inline AI insight cards. Supports sorting by impact, recency, or trending velocity.
- **`/trends` — Technology Radar:** Visual matrix plotting technical domains across the **Hype vs. Adoption** plane (arXiv research volume vs. GitHub implementation velocity), accompanied by 7-day volume sparklines and weekly comparison bars.
- **`/item/:id` — Deep-Dive Item View:** Full technical profile with complete abstract/README, metadata table, AI executive summary, key takeaways, and a feature attribution bar chart breaking down why the model scored it the way it did.
- **`/evaluation` — Model Evaluation & Faculty Review:** Transparent scorecard showing exact 5-fold cross-validation RMSEs, baseline vs. XGBoost comparisons, classification accuracy reports, and live pipeline error telemetry.

---

## Repository Structure

```
TechPulse-AI/
├── backend/
│   └── app/
│       ├── api/            # FastAPI routes: /feed, /item, /trends, /search, /health, /evaluation
│       ├── core/           # Database sessions, Redis cache client & fallbacks, config
│       ├── ml/             # FeatureExtractor, ML inference engine, TreeSHAP explainer
│       ├── models/         # SQLAlchemy ORM models (Item, Classification, Prediction, Insight...)
│       ├── schemas/        # Pydantic validation schemas
│       ├── services/       # External clients (arXiv, GitHub, Hacker News, Semantic Scholar, LLM)
│       ├── tasks/          # 6-stage autonomous Celery pipeline workers & runner
│       └── main.py         # FastAPI application entrypoint & middleware
├── Frontend/
│   ├── src/
│   │   ├── api/            # Axios API client functions
│   │   ├── components/     # UI components (Feed, Radar Matrix, Explainability Widgets, Shell)
│   │   ├── pages/          # DashboardPage, TrendsPage, ItemDetailPage, EvaluationPage
│   │   ├── store/          # Zustand global feed state (filters, search query, active domain)
│   │   └── App.jsx         # Client-side router configuration
├── Data/                   # Seed datasets (arXiv, GitHub, Hacker News) & training exports
├── Docs/                   # PRD, TRD, design specifications, and architecture guides
├── models/                 # Serialized XGBoost models (.pkl), scalers, and domain configs
├── ml_reports/             # Benchmark JSON reports (CV RMSE, classification evaluation)
├── model_decision_trees/   # Markdown dumps of model tree logic for auditability
├── scripts/
│   ├── run_phase1_pipeline.py         # Full Phase 1 data collection & model training runner
│   ├── train_prediction_models.py     # XGBoost + Ridge + Random Forest training & CV
│   ├── test_pipeline_e2e.py           # End-to-end 7-step autonomous pipeline test suite
│   ├── seed_database.py               # Database initialization & sample seeding
│   └── export_decision_trees_markdown.py # Exports decision tree structures to markdown
├── .env.example            # Environment configuration template
└── README.md
```

---

## Verification & Automated Tests

To run the complete Phase 3 end-to-end test suite (which tests live ingestion, deduplication, Semantic Scholar enrichment, classification, XGBoost inference, TreeSHAP feature drivers, LLM synthesis, trend aggregation, error handling, and API responses):

```bash
python scripts/test_pipeline_e2e.py
```

Expected result:
```
🧪 ATIP PHASE 3: END-TO-END PIPELINE VERIFICATION SUITE
  ✅ Pipeline executed successfully
  ✅ Deduplication verified
  ✅ TreeSHAP explainability drivers verified
  ✅ Structured AI insight schema verified
  ✅ Technology Radar metrics aggregated
  ✅ Error audit log verified in pipeline_errors table
  ✅ FastAPI feed & search verified
🎉 ALL PHASE 3 END-TO-END PIPELINE TESTS PASSED WITH ZERO ERRORS!
```

---

## Team & Credits

Developed as part of the Machine Learning initiative at **IoT Lab, Campus 25, KIIT University**:

- **Sagnik Pramanik** — POC & Machine Learning Lead (Model architectures, training, evaluation)
- **Udit Kumar Jaiswal** — Data Engineering & MLOps (Ingestion pipelines, feature engineering, enrichment)
- **Shadwal Singh** — Backend & Infrastructure (FastAPI, database schema, caching, search)
- **Pragati Singh** — Frontend Development (React dashboard, Technology Radar, UI components)

---

## License

This project is open-source under the [MIT License](LICENSE).
