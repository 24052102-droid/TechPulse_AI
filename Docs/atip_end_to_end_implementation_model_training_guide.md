# ATIP (TechPulse AI) — Step-by-Step Model Training & End-to-End Implementation Guide

**Project:** Autonomous Technical Intelligence & Prediction Platform (ATIP / TechPulse AI)  
**Institution:** IoT Lab — Machine Learning · Campus 25, KIIT University  
**Team Roles:** Sagnik Pramanik (POC & ML Lead) · Udit Kumar Jaiswal (Data Eng & MLOps) · Shadwal Singh (Backend & Infra) · Pragati Singh (Frontend)

---

## Overview of the Implementation Sequence

In an AI/ML intelligence platform, **you cannot deploy an inference pipeline until your classification and supervised regression models are benchmarked, calibrated, and serialized**. Furthermore, as highlighted in the **TechPulse AI Brief** and **Risk `R-01` (Data Cold-Start)** of the PRD, training a model to predict $180$-day paper citations or $30$-day GitHub star velocity requires historical snapshots where the outcome is already observable.

This guide is structured into **five sequential phases**:
1. **Phase 1 (The First Step): Data Collection, Feature Engineering & Model Training** — Solving the cold-start problem, preventing data leakage, benchmarking the domain classifier ($\ge 85\%$ accuracy), and training the supervised XGBoost & baseline models ($\text{RMSE} \le 0.20$).
2. **Phase 2: Database & Broker Infrastructure Setup** — Provisioning PostgreSQL 15 (Supabase), Redis 7 (Upstash), and the FastAPI + Celery monorepo.
3. **Phase 3: The 6-Stage Autonomous Processing Workflow** — Implementing the daily Celery Beat pipeline from raw API ingestion to domain trend aggregation.
4. **Phase 4: Backend API & User Request Flows** — Building the cached feed, lazy-loaded LLM insight polling, and hybrid full-text search endpoints.
5. **Phase 5: Frontend Integration, Deployment & Faculty Evaluation** — Connecting the minimalist UI and verifying all non-functional requirements (`NFR-01` to `NFR-10`).

---

## PHASE 1 (FIRST STEP): Historical Data Collection, Feature Engineering & Model Training

**Primary Owners:** Sagnik Pramanik (ML Lead) & Udit Kumar Jaiswal (Data Engineering)  
**Compute Environment:** Google Colab (T4 GPU for BART/DistilBERT) + Local Python $3.11$ environment  
**Output Artifacts:**
* `models/domain_classifier_config.json` & `ml_reports/classification_eval_{date}.json`
* `models/paper_impact_xgb_v1.pkl` & `models/paper_feature_scaler_v1.pkl`
* `models/repo_growth_xgb_v1.pkl` & `models/repo_feature_scaler_v1.pkl`
* `models/domain_trend_logreg_v1.pkl`

---

### Step 1.1: Solving the Cold-Start Problem (Constructing the Historical Training Dataset)

Because you cannot wait $6$ months after Project Day 1 to observe future citations or star growth, you must construct a **retrospective time-anchored dataset** where features are reconstructed at a past timestamp $t_0$ and target labels are measured at $t_0 + \Delta t$.

#### A. Historical arXiv + Semantic Scholar Dataset ($N = 3,000$ Papers)
1. **Select the Historical Window:** Query the arXiv API (`http://export.arxiv.org/api/query`) for papers submitted between **$7$ and $18$ months ago** across the $7$ target CS categories: `cs.LG`, `cs.CV`, `cs.CL`, `cs.RO`, `cs.CR`, `cs.SY`, and `eess.SP`.
2. **Enrich with Semantic Scholar Outcomes:** For each historical `arxiv_id`, query the Semantic Scholar Graph API:
   ```text
   GET https://api.semanticscholar.org/graph/v1/paper/arXiv:{arxiv_id}?fields=title,abstract,authors.hIndex,citationCount,influentialCitationCount,publicationDate,citations.year
   ```
3. **Define Snapshot Features ($t_0$) vs. Target Outcome ($t_0 + 180\text{d}$):**
   * **Input Features at $t_0$ (Submission Date):** Title, abstract text, author count, maximum author $h$-index, arXiv primary category, presence of a GitHub URL in the abstract, and Flesch-Kincaid readability score. *(Crucial Safeguard: Never include `citationCount` or `influentialCitationCount` as an input feature for a newly published paper, as a new paper has $0$ citations at $t_0$).*
   * **Target Variable ($y_{\text{paper}}$):** Citations accumulated within $180$ days of publication. Apply a log-transformation followed by Min-Max normalization onto $[0, 1]$ so extreme viral outlier papers do not skew regression gradients:
     $$z_i = \ln(1 + \text{citations}_{180\text{d}, i})$$
     $$y_{\text{paper}, i} = \frac{z_i - \min(z)}{\max(z) - \min(z)} \in [0, 1]$$

#### B. Historical GitHub Repository Dataset ($N = 2,000$ Repositories)
1. **Two-Pronged Collection Strategy:**
   * **Day-1 Live Snapshot Logger:** Start a daily cron script immediately on Day 1 that saves `(repo_id, date, stargazers_count, forks_count, open_issues_count)` for $1,500$ active ML repositories (`topic:machine-learning`, `topic:deep-learning`, `topic:llm`).
   * **Retrospective Star Velocity Reconstruction (For Immediate Model Training):** Use the GitHub Stargazers API with header `Accept: application/vnd.github.v3.star+json` (which returns `starred_at` timestamps) or GH Archive BigQuery public dataset to reconstruct a repository's state at $t_0 = \text{Today} - 30\text{ days}$ and compute the exact stars gained over $[t_0, t_0 + 30\text{d}]$.
2. **Target Variable ($y_{\text{repo}}$):** Stars gained in the $30$-day window $\Delta S_{30\text{d}} = \max(0, S_{t_0 + 30\text{d}} - S_{t_0})$, log-transformed and normalized to $[0, 1]$:
   $$w_i = \ln(1 + \Delta S_{30\text{d}, i}), \quad y_{\text{repo}, i} = \frac{w_i - \min(w)}{\max(w) - \min(w)} \in [0, 1]$$

---

### Step 1.2: Domain Classification Benchmarking & Validation (Target: Accuracy $\ge 85\%$, Macro $F_1 \ge 0.80$)

Before training the impact predictors, the classification layer must be validated because `domain_confidence` and `primary_domain` feed into downstream ML features.

#### 1. Define the Deterministic Category-to-Domain Mapping (Ground Truth for $n = 500$ Test Set)
Create a held-out evaluation dataset of $500$ arXiv papers ($50$ per domain) using known arXiv primary categories and keyword filters as ground truth:

| ATIP Domain Label | Ground-Truth arXiv Category / Filter |
| :--- | :--- |
| `Natural Language Processing` | `cs.CL` |
| `Computer Vision` | `cs.CV` |
| `Reinforcement Learning` | `cs.LG` + abstract contains `"reinforcement learning"` / `"MDP"` / `"policy gradient"` |
| `IoT and Embedded Systems` | `eess.SP` / `cs.AR` + edge/embedded keywords |
| `Systems and Infrastructure` | `cs.SY` / `cs.DC` / `cs.OS` |
| `Robotics` | `cs.RO` |
| `Security and Privacy` | `cs.CR` |
| `General Machine Learning` | `cs.LG` / `stat.ML` (excluding RL/Multimodal subsets) |
| `Data Engineering and Pipelines` | `cs.DB` + data pipeline / vector index keywords |
| `Multimodal and Foundation Models` | `cs.CL` + `cs.CV` cross-listed or `"multimodal"` / `"VLM"` |

#### 2. Run Zero-Shot Inference & Evaluate Metrics
Execute the following evaluation script on Google Colab (GPU) to benchmark `facebook/bart-large-mnli`:

```python
from transformers import pipeline
from sklearn.metrics import accuracy_score, f1_score, classification_report
import json

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

classifier = pipeline(
    "zero-shot-classification",
    model="facebook/bart-large-mnli",
    device=0  # Use GPU on Colab
)

def classify_batch(items: list[dict]) -> list[dict]:
    texts = [f"{item['title']} . {item['description'][:600]}" for item in items]
    outputs = classifier(texts, candidate_labels=DOMAIN_LABELS, multi_label=False)
    
    results = []
    for item, out in zip(items, outputs):
        labels, scores = out["labels"], out["scores"]
        primary_domain = labels[0]
        primary_score = scores[0]
        secondary_domains = [
            lbl for lbl, scr in zip(labels[1:3], scores[1:3]) if scr > 0.15
        ]
        results.append({
            "item_id": item["id"],
            "primary_domain": primary_domain,
            "secondary_domains": secondary_domains,
            "confidence_scores": {
                lbl: round(scr, 4) for lbl, scr in zip(labels, scores) if scr >= 0.05
            },
            "low_confidence": primary_score < 0.35
        })
    return results
```

#### 3. Ensemble Fallback Protocol (Risk `R-02`)
* Compute Top-1 Accuracy and Macro $F_1$ on the $500$-paper test set.
* **If Top-1 Accuracy $< 0.85$:** Fine-tune `distilbert-base-uncased` (or `sentence-transformers/all-MiniLM-L6-v2` + `LogisticRegression` head, as recommended in the TechPulse AI Brief Page 6) on $2,000$ labeled abstracts and take a weighted probability ensemble:
  $$P_{\text{ensemble}}(c \mid x) = 0.6 \cdot P_{\text{DistilBERT}}(c \mid x) + 0.4 \cdot P_{\text{BART}}(c \mid x)$$
* Save the final evaluation metrics to `ml_reports/classification_eval_2026_10.json` so the `/evaluation` frontend page can render the exact per-domain precision, recall, and $F_1$ table.

---

### Step 1.3: Feature Engineering Pipeline (`FeatureExtractor`)

Create a deterministic, reusable `FeatureExtractor` module (`backend/app/ml/features.py`) that is shared identically between **offline training** and **online Celery inference** (preventing training-serving skew).

```python
import math
from datetime import datetime, timezone
import textstat

ARXIV_CATEGORIES = ["cs.LG", "cs.CV", "cs.CL", "cs.RO", "cs.CR", "cs.SY", "eess.SP"]
LICENSES = ["MIT", "Apache-2.0", "GPL-3.0", "none", "other"]
LANGUAGES = ["Python", "JavaScript", "TypeScript", "Rust", "Go", "C++", "other"]

class FeatureExtractor:
    @staticmethod
    def extract_arxiv_features(item: dict, classification_score: float, snapshot_time: datetime) -> dict:
        title = item.get("title", "")
        abstract = item.get("description", "")
        meta = item.get("metadata", {})
        authors = meta.get("authors", [])
        categories = meta.get("categories", [])
        
        created_at = item.get("created_at") or snapshot_time
        days_since_sub = max(0, (snapshot_time - created_at).days)
        
        features = {
            "title_word_count": len(title.split()),
            "abstract_word_count": len(abstract.split()),
            "flesch_score": textstat.flesch_reading_ease(abstract) if abstract else 50.0,
            "domain_confidence": float(classification_score),
            "author_count": len(authors),
            "max_author_hindex": float(meta.get("max_h_index", 0)),
            "days_since_submission": days_since_sub,
            "has_code_link": int("github.com" in abstract.lower() or "code available" in abstract.lower()),
            "num_figures": int(meta.get("num_figures", 0)),
        }
        # One-hot encode 7 arXiv categories
        for cat in ARXIV_CATEGORIES:
            features[f"cat_{cat}"] = int(cat in categories)
        return features

    @staticmethod
    def extract_github_features(item: dict, classification_score: float, snapshot_time: datetime) -> dict:
        meta = item.get("metadata", {})
        stars = max(int(meta.get("stargazers_count", 1)), 1)
        forks = int(meta.get("forks_count", 0))
        pushed_at = meta.get("pushed_at", snapshot_time)
        days_since_commit = max(0, (snapshot_time - pushed_at).days) if isinstance(pushed_at, datetime) else 1
        
        lic = meta.get("license") or "none"
        lic_norm = lic if lic in LICENSES else "other"
        
        lang = meta.get("language") or "other"
        lang_norm = lang if lang in LANGUAGES else "other"
        
        features = {
            "stars_log": math.log1p(stars),
            "forks": forks,
            "fork_star_ratio": round(forks / stars, 4),
            "open_issues": int(meta.get("open_issues_count", 0)),
            "readme_length": len(meta.get("readme_snippet", "")),
            "topic_count": len(meta.get("topics", [])),
            "days_since_commit": days_since_commit,
            "domain_confidence": float(classification_score),
        }
        for l_val in LICENSES:
            features[f"lic_{l_val}"] = int(lic_norm == l_val)
        for lg_val in LANGUAGES:
            features[f"lang_{lg_val}"] = int(lang_norm == lg_val)
        return features
```

---

### Step 1.4: Time-Based Split, Baseline Comparison & XGBoost Training

Per **Section 6 & 9 of the TechPulse AI Brief**, you must:
1. **Split by Time (Not Random Shuffle):** Sort historical items chronologically by `created_at`. Use the oldest $70\%$ for Training, the next $10\%$ for Validation, and the most recent $20\%$ as the untouched Time-Holdout Test Set.
2. **Compare Against a Simple Baseline:** Train a `Ridge` / `LinearRegression` baseline and a `RandomForestRegressor` alongside `XGBRegressor` to prove that gradient boosting provides a genuine lift.
3. **Run 5-Fold Cross-Validation:** Verify that the normalized $\text{RMSE} \le 0.20$:
   $$\text{RMSE} = \sqrt{\frac{1}{N} \sum_{i=1}^{N} \left(\hat{y}_i - y_i\right)^2} \le 0.20$$

#### Training & Explainability Script (`scripts/train_prediction_models.py`):

```python
import joblib
import numpy as np
import pandas as pd
from xgboost import XGBRegressor
from sklearn.linear_model import Ridge
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import KFold
from sklearn.metrics import root_mean_squared_error, r2_score

def train_and_evaluate(df: pd.DataFrame, feature_cols: list[str], target_col: str, task_name: str):
    # 1. Chronological Time Split (80% Train/CV, 20% Later Time Holdout)
    df = df.sort_values("created_at").reset_index(drop=True)
    split_idx = int(len(df) * 0.8)
    train_df, test_df = df.iloc[:split_idx], df.iloc[split_idx:]
    
    X_train, y_train = train_df[feature_cols], train_df[target_col]
    X_test, y_test = test_df[feature_cols], test_df[target_col]
    
    # 2. Baseline Model (Ridge Linear Regression)
    baseline = Ridge(alpha=1.0)
    baseline.fit(X_train, y_train)
    base_preds = np.clip(baseline.predict(X_test), 0.0, 1.0)
    base_rmse = root_mean_squared_error(y_test, base_preds)
    
    # 3. 5-Fold Cross Validation on XGBoost Regressor
    kf = KFold(n_splits=5, shuffle=True, random_state=42)
    cv_rmses, cv_r2s = [], []
    
    for tr_idx, val_idx in kf.split(X_train):
        model_cv = XGBRegressor(
            n_estimators=300, max_depth=6, learning_rate=0.05,
            subsample=0.8, colsample_bytree=0.8, random_state=42
        )
        model_cv.fit(X_train.iloc[tr_idx], y_train.iloc[tr_idx])
        val_preds = np.clip(model_cv.predict(X_train.iloc[val_idx]), 0.0, 1.0)
        cv_rmses.append(root_mean_squared_error(y_train.iloc[val_idx], val_preds))
        cv_r2s.append(r2_score(y_train.iloc[val_idx], val_preds))
        
    # 4. Fit Final XGBoost Model on Full Training Split & Evaluate on Time Holdout
    final_xgb = XGBRegressor(
        n_estimators=300, max_depth=6, learning_rate=0.05,
        subsample=0.8, colsample_bytree=0.8, random_state=42
    )
    final_xgb.fit(X_train, y_train)
    test_preds = np.clip(final_xgb.predict(X_test), 0.0, 1.0)
    test_rmse = root_mean_squared_error(y_test, test_preds)
    test_r2 = r2_score(y_test, test_preds)
    
    print(f"[{task_name}] Baseline RMSE: {base_rmse:.4f} | XGBoost 5-Fold CV RMSE: {np.mean(cv_rmses):.4f} (±{np.std(cv_rmses):.4f}) | Holdout RMSE: {test_rmse:.4f} | R2: {test_r2:.4f}")
    
    # Save artifact
    joblib.dump({
        "model": final_xgb,
        "feature_cols": feature_cols,
        "cv_rmse_mean": float(np.mean(cv_rmses)),
        "holdout_rmse": float(test_rmse),
        "baseline_rmse": float(base_rmse),
        "model_version": f"{task_name}_xgb_v1.0"
    }, f"models/{task_name}_xgb_v1.pkl")
```

#### Computing Per-Item Top 3 Feature Drivers (For UI Explainability Tooltips)
Both the PRD (`F-03`: *"Tooltip on hover: lists the top 3 features that drove the score"*) and the TechPulse Brief require per-item feature attribution. During inference, use XGBoost's native `pred_contribs=True` (exact TreeSHAP values) so every prediction stores its top $3$ positive contributors in `predictions.features_used`:

```python
import xgboost as xgb

def predict_with_explanations(artifact: dict, feature_dict: dict) -> dict:
    model: XGBRegressor = artifact["model"]
    cols: list[str] = artifact["feature_cols"]
    X_row = pd.DataFrame([feature_dict])[cols]
    
    raw_score = float(np.clip(model.predict(X_row)[0], 0.0, 1.0))
    score_display = round(raw_score * 10.0, 1)
    
    # Extract exact SHAP feature contributions via XGBoost booster
    dmat = xgb.DMatrix(X_row, feature_names=cols)
    contribs = model.get_booster().predict(dmat, pred_contribs=True)[0][:-1]  # Exclude bias term
    
    top_indices = np.argsort(np.abs(contribs))[::-1][:3]
    top_drivers = [
        {"feature": cols[idx], "value": feature_dict[cols[idx]], "impact": round(float(contribs[idx]), 3)}
        for idx in top_indices
    ]
    return {
        "score": round(raw_score, 4),
        "score_display": score_display,
        "top_drivers": top_drivers,
        "model_version": artifact["model_version"]
    }
```

---

### Step 1.5: Training Task 3 — Domain Trend Classifier (`LogisticRegression`)

1. **Aggregate Historical Daily Counts:** Using the $30$-day backfilled item counts per domain, compute for each `(domain, date)`:
   * `rolling_7d_count`: $\sum_{k=0}^{6} \text{count}_{t-k}$
   * `rolling_7d_avg_impact`: $\frac{1}{7} \sum_{k=0}^{6} \overline{\text{score}}_{t-k}$
   * `wow_delta`: $\frac{\text{rolling\_7d\_count}_t - \text{rolling\_7d\_count}_{t-7}}{\max(1, \text{rolling\_7d\_count}_{t-7})}$
2. **Define Binary Target:** $y_{\text{trend}} = 1$ if $\text{wow\_delta} > 0.20$ ($>20\%$ week-over-week growth), else $0$.
3. **Train & Save:** Fit a calibrated `LogisticRegression` model (`scikit-learn`) and save to `models/domain_trend_logreg_v1.pkl`.

---

## PHASE 2: Storage, Database & Broker Infrastructure Setup

**Primary Owner:** Shadwal Singh (Full-Stack & Infra)

### Step 2.1: Initialize Monorepo Structure
```text
atip-platform/
├── backend/
│   ├── app/
│   │   ├── api/            # FastAPI routers (feed, item, trends, search, health)
│   │   ├── core/           # Config, DB session, Redis client
│   │   ├── ml/             # FeatureExtractor, Classifier wrapper, XGBoost loader
│   │   ├── services/       # ArXiv, GitHub, HN, Semantic Scholar, Anthropic LLM clients
│   │   └── tasks/          # Celery app, celery_config.py, pipeline worker tasks
│   ├── models/             # Git LFS tracked .pkl artifacts from Phase 1
│   ├── ml_reports/         # Classification & regression benchmark JSONs
│   └── requirements.txt
├── frontend/               # React 18 + Vite + TailwindCSS + Zustand + Recharts
└── .github/
    ├── CODEOWNERS          # Maps Pragati's components for probation evaluation
    └── workflows/ci.yml    # Automated test + lint + deploy
```

### Step 2.2: Provision PostgreSQL 15 (Supabase) & Full-Text Search Indexes
Run the SQL migration on Supabase to create the $5$ core tables (`items`, `classifications`, `insights`, `predictions`, `domain_trends`) plus the `pipeline_errors` table and a generated `tsvector` index for sub-$500\text{ms}$ search (`NFR-02`):

```sql
-- Enable UUID extension
CREATE EXTENSION IF NOT EXISTS "pgcrypto";

-- 1. Core tables as defined in TRD (items, classifications, insights, predictions, domain_trends)
-- Add full-text search index on items for /api/search:
ALTER TABLE items ADD COLUMN IF NOT EXISTS search_vector tsvector
GENERATED ALWAYS AS (
    setweight(to_tsvector('english', coalesce(title, '')), 'A') ||
    setweight(to_tsvector('english', coalesce(description, '')), 'B')
) STORED;

CREATE INDEX idx_items_search_vector ON items USING GIN (search_vector);

-- 2. Pipeline error monitoring table for NFR-09
CREATE TABLE pipeline_errors (
    id          UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    task_name   VARCHAR(100) NOT NULL,
    item_id     UUID REFERENCES items(id) ON DELETE SET NULL,
    error_msg   TEXT NOT NULL,
    occurred_at TIMESTAMPTZ DEFAULT NOW()
);
```

### Step 2.3: Provision Upstash Redis 7
Configure Redis for three isolated key namespaces:
1. `celery://*` — Celery task broker and result backend.
2. `llm:insight:{sha256_hash}` — Indefinite TTL cache (`TTL = None`) for LLM JSON outputs (`NFR-06`).
3. `api:feed:{sort}:{domains_hash}:p{page}` — $5$-minute TTL cache (`TTL = 300s`) for FastAPI feed queries (`NFR-01`).

---

## PHASE 3: Detailed Execution of the 6-Stage Autonomous Pipeline

**Primary Owners:** Udit Kumar Jaiswal (Stages 1, 2, 6) & Sagnik Pramanik (Stages 3, 4, 5)

The entire backend processing workflow is orchestrated via **Celery Canvas chains** and scheduled by **Celery Beat**:

```text
[Stage 1: Ingestion (00:30-01:30 IST)]
       │
       ▼
[Stage 2: Semantic Scholar Enrichment & Repo Matching]
       │
       ▼
[Stage 3: BART/DistilBERT Batch Classification (Batch = 10)]
       │
       ├───────────────────────────────────────────┐
       ▼                                           ▼
[Stage 4: XGBoost Prediction & SHAP Drivers]  [Stage 5: LLM Synthesis & Redis Caching (Batch = 20)]
       │                                           │
       └───────────────────┬───────────────────────┘
                           ▼
[Stage 6: Daily Domain Trend & Tech Radar Aggregation (02:00 IST)]
```

---

### Stage 1: Autonomous Multi-Source Ingestion (`tasks/ingest.py`)
1. **`fetch_arxiv_papers()` (Cron: `00:30 IST` daily):**
   * Queries `http://export.arxiv.org/api/query` across `cs.LG`, `cs.CV`, `cs.CL`, `cs.RO`, `cs.CR`, `cs.SY`, `eess.SP` ($\sim 200$ papers/day).
   * Enforces rate limit ($\le 3\text{ req/s}$) and exponential backoff ($2^n\text{ minutes}$, `max_retries=3`).
   * Extracts `paper_id`, `title`, `authors`, `abstract`, `categories`, `submitted_date`, `pdf_link` and regex-scans the abstract for any `https://github.com/[owner]/[repo]` implementation link.
2. **`fetch_github_repos()` (Cron: `01:00 IST` daily):**
   * Queries `https://api.github.com/search/repositories` authenticated with a `GITHUB_PAT` ($5,000\text{ req/hr}$) for `stars:>100 pushed:>[YESTERDAY]` across rotating ML topics ($\sim 150$ repos/day).
   * Calls `/repos/{owner}/{repo}/readme`, base64-decodes the markdown, and extracts the first $600$ clean characters into `metadata.readme_snippet`.
3. **`fetch_hn_stories()` (Cron: Every $6\text{ hours}$):**
   * Queries `https://hn.algolia.com/api/v1/search?tags=story` with `points >= 20` and valid external URLs across rotated ML/AI keywords ($\sim 50$ stories/day).
4. **Normalization & Deduplication:**
   * Converts every fetched record into the Pydantic `RawItem` schema and performs a bulk upsert:
     ```sql
     INSERT INTO items (source, source_id, title, description, url, metadata, created_at)
     VALUES (...) ON CONFLICT (source_id) DO NOTHING RETURNING id;
     ```
   * Only **net-new `item.id` UUIDs** are passed downstream to Stage 2 and Stage 3.

---

### Stage 2: Semantic Scholar Enrichment (`tasks/enrich.py`)
1. Triggered automatically for all newly inserted `source = 'arxiv'` items.
2. Calls `https://api.semanticscholar.org/graph/v1/paper/arXiv:{source_id}?fields=citationCount,influentialCitationCount,authors.hIndex,year` respecting the $100\text{ req/5 min}$ limit.
3. Computes `max_h_index = max([a.get("hIndex", 0) for a in authors], default=0)` and updates `items.metadata` in PostgreSQL via `jsonb_set`.

---

### Stage 3: Domain Classification Task (`tasks/classify.py`)
1. Selects all rows in `items` where no corresponding record exists in `classifications`.
2. Groups items into **batches of $10$** and constructs the input string `f"{title} . {description[:600]}"`.
3. Runs inference through the validated classifier from **Step 1.2**:
   * Top-1 label is assigned to `primary_domain`.
   * Ranks $2$ and $3$ with score $> 0.15$ are stored in `secondary_domains[]`.
   * All scores $\ge 0.05$ are stored in `confidence_scores` JSONB (`{"NLP": 0.91, "Multimodal AI": 0.18}`).
   * If `max(scores) < 0.35`, sets `low_confidence = TRUE` for review.
   * Also detects whether any metric spiked in the last $48$ hours and flags `metadata.is_rising = true`.

---

### Stage 4: Feature Extraction & Supervised ML Prediction (`tasks/predict.py`)
1. Triggered immediately after Stage 3 completes (`WHERE classification IS NOT NULL AND prediction IS NULL`).
2. Loads the cached `.pkl` model artifacts (`paper_impact_xgb_v1.pkl` and `repo_growth_xgb_v1.pkl`) into worker memory once at Celery startup.
3. Calls `FeatureExtractor.extract_arxiv_features()` or `FeatureExtractor.extract_github_features()`. *(For Hacker News items, computes a normalized velocity score based on `points / hours_since_submission` combined with domain weight).*
4. Runs `predict_with_explanations()` (from **Step 1.4**) to produce:
   * `score` $\in [0.0, 1.0]$
   * `score_display` $\in [0.0, 10.0]$
   * `features_used` JSONB containing the raw feature values AND the `top_drivers` list so the UI tooltip and `/item/:id` explainability bar chart render instantaneously without recomputing SHAP on the fly.

---

### Stage 5: LLM Insight Generation & Caching (`tasks/insights.py`)
1. Runs concurrently with Stage 4 for P0 classified items (`WHERE insight IS NULL`), grouped into **batches of $20$**.
2. **Cache-First Guardrail (`NFR-06`):**
   * Computes `cache_key = f"llm:insight:{sha256(f'{source_id}:{MODEL_VERSION}')}"`.
   * Checks Upstash Redis via `redis.get(cache_key)`. On a cache hit, inserts directly into PostgreSQL `insights` without making an external API call.
3. **Structured Prompt Execution:**
   * Calls `claude-sonnet-4-6` (or `gpt-4o-mini` if daily token spend in `llm_usage` approaches $₹50/\text{day}$) using the strict JSON schema prompt template.
   * Extracts `summary` ($3$ sentences), `key_takeaways` ($3$ bullets), `why_it_matters` ($1$ paragraph), `technical_depth` (`beginner` | `intermediate` | `advanced`), `estimated_read_time_minutes`, and `related_topics` ($3$ tags).
   * Validates the response with Pydantic. If JSON parsing fails, retries once with a stricter system prompt; if it fails twice, logs to `pipeline_errors` and leaves the item functional with its classification and impact score (`Degrade Gracefully` principle).

---

### Stage 6: Daily Domain Trend & Technology Radar Aggregation (`tasks/trends.py`)
1. Runs daily at `02:00 IST` after Stages $3\text{–}5$ finish.
2. Executes an aggregation query grouping items by `primary_domain` and `DATE(ingested_at)`:
   * Computes `item_count` and `avg_impact = AVG(predictions.score_display)`.
   * Calculates the $7$-day linear regression slope (`trend_score`) over $[t-6, t]$ using `np.polyfit(range(7), counts_7d, 1)[0]`.
   * Computes week-over-week growth: if $\frac{\text{count}_{7\text{d}} - \text{count}_{\text{prev\_7d}}}{\max(1, \text{count}_{\text{prev\_7d}})} > 0.20$, sets `is_trending = TRUE`.
   * Computes the **Hype vs. Adoption ratio** (ratio of arXiv paper growth to GitHub repository growth within each domain) for the `/trends` Technology Radar view.
3. Upserts results into `domain_trends` via `ON CONFLICT (domain, date) DO UPDATE`.

---

## PHASE 4: Backend API Layer & User Request Flows

**Primary Owner:** Shadwal Singh

### 1. Main Intelligence Feed (`GET /api/feed`)
* **Query Params:** `domain` (comma-separated list), `source` (`arxiv` | `github` | `hn`), `sort` (`impact_score` | `recent` | `trending`), `page` ($\ge 1$), `limit` ($20$).
* **Flow:**
  1. Checks Redis key `api:feed:{sort}:{domains}:{source}:p{page}`. Returns cached JSON in $< 15\text{ms}$ if present.
  2. On cache miss, executes a single indexed `LEFT JOIN` across `items`, `classifications`, `predictions`, and `insights` (selecting only metadata, scores, tags, and whether insights are ready).
  3. Serializes via Pydantic v2 and caches in Redis with `TTL = 300` seconds.

### 2. Lazy-Loaded Insight Expansion (`GET /api/item/{id}/insights`)
* **Flow:**
  1. When a user clicks **`[View AI Insights ▾]`** on an `<ItemCard />`, the frontend calls `GET /api/item/{id}/insights`.
  2. If the row exists in the `insights` table (or Redis cache), FastAPI returns `200 OK` immediately.
  3. If the row is missing, FastAPI enqueues `generate_single_insight.delay(item_id)` on Celery and returns `202 Accepted` with `{"status": "processing", "task_id": "..."}`.
  4. The frontend displays the minimalist skeleton loader and polls every $3\text{ seconds}$ until `200 OK` is returned, then caches the result indefinitely in TanStack Query (`staleTime: Infinity`).

### 3. Hybrid Full-Text + Impact Reranked Search (`GET /api/search`)
* **Query Params:** `q` (natural language query), `domain`, `sort`, `page`.
* **Ranking Formula:** Combines PostgreSQL `ts_rank` text relevance ($40\%$ weight) with the normalized ML impact score ($60\%$ weight):
  $$\text{CombinedRank} = 0.4 \times \text{ts\_rank}(\text{search\_vector}, \text{plainto\_tsquery}(q)) + 0.6 \times \text{predictions.score}$$
* **Performance:** Uses the `GIN` index created in Phase 2 to guarantee $p_{95} < 500\text{ms}$ (`NFR-02`).

### 4. Telemetry & Model Evaluation Endpoint (`GET /api/health` & `GET /api/evaluation`)
* Exposes live PostgreSQL item count, Redis cache hit ratio, last successful Celery ingestion timestamp, and serves the saved JSON evaluation report (`ml_reports/classification_eval.json` and XGBoost holdout RMSE metrics) for the `/evaluation` page.

---

## PHASE 5: Minimalist Frontend Integration & Faculty Evaluation Checklist

**Primary Owners:** Pragati Singh (Frontend Components) & Sagnik Pramanik (POC Integration & Demo)

### Step 5.1: Implementing the Minimalist UI (`sitemap.md` & `design.md`)
1. **Global State (`useFeedStore.js` in Zustand):** Synchronize `selectedDomains[]`, `selectedSource`, `sortBy`, and `searchQuery` with URL search parameters so every filtered view is bookmarkable and shareable.
2. **Component Ownership (`CODEOWNERS` Compliance for `F-08`):**
   * Pragati builds and commits `<ItemCard />`, `<InsightPanel />`, `<ImpactScoreBar />`, `<SidebarDomainFilter />`, and `<TrendsPage />` under scoped branches (`feature/pragati-item-card`, `feature/pragati-insight-panel`, `feature/pragati-trends-page`).
3. **Explainable Micro-Interactions:**
   * Wire the `<ImpactScoreBar />` hover popover to `prediction.features_used.top_drivers` so hovering over any score displays the exact top $3$ XGBoost SHAP contributors.
   * Wire the `<DomainTag />` hover tooltip to `classification.confidence_scores[primary_domain]`.

### Step 5.2: Pre-Review Verification Checklist (48 Hours Before Faculty Demo)

| Requirement ID | Verification Check | Target Threshold |
| :--- | :--- | :--- |
| **`NFR-01`** | Run Chrome Lighthouse audit on deployed Vercel URL (`/`) | Load time $< 2.0\text{s}$ on 4G |
| **`NFR-02`** | Run search query `"transformer"` and inspect FastAPI timing header | $p_{95} < 500\text{ms}$ |
| **`NFR-04`** | Inspect `/evaluation` Classification Scorecard | Top-1 Accuracy $\ge 85\%$, Macro $F_1 \ge 0.80$ |
| **`NFR-05`** | Inspect `/evaluation` Regression Scorecard | 5-Fold CV $\text{RMSE} \le 0.20$ |
| **`NFR-06`** | Verify Redis insight cache hit rate on P0 feed items | $100\%$ of P0 items cached; spend $< ₹500/\text{mo}$ |
| **`NFR-08`** | Check GitHub Insights $\rightarrow$ Contributors graph | All $4$ members have $\ge 10$ scoped commits |
| **`R-04`** | Verify Render web service + local `docker-compose` fallback | Both live URL and local fallback operational |