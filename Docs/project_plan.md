# ATIP (TechPulse AI) — Phase 1 Model Training Plan

> [!IMPORTANT]
> This plan covers **Phase 1 only** — the critical first step before any backend/frontend work can begin. Models must be trained, validated, and serialized before the inference pipeline can be deployed.

## 📊 Current Data Inventory

| Dataset | Location | Records | Key Columns |
|---------|----------|---------|-------------|
| arXiv Papers (metadata) | `Data/data 1 research paper/paper_metadata.csv` | 46 papers | paper_id, title, authors, categories, published_date, abstract |
| arXiv Papers (full text segments) | `Data/data 2 research paper/combined_research_dataset.csv` | 30,236 segments | paper_id, title, categories, section, content |
| Hacker News (QA pairs) | `Data/data 3 hacker news/all_15_topics_combined.csv` | 7,500 records | id, topic, question, answer, source_title, source_url, difficulty |
| GitHub Repos | `Data/data 5 github/techpulse.db` (SQLite) | 8,679 repos + 8,679 snapshots | full_name, description, stars, forks, open_issues, language, license, topics |

## 🎯 Phase 1 Execution Steps

### Step 1: Install Dependencies & Setup Environment
- Install: `xgboost`, `scikit-learn`, `textstat`, `joblib`, `scipy`, `matplotlib`, `seaborn`
- Create project directories: `models/`, `ml_reports/`, `scripts/`, `backend/app/ml/`

### Step 2: Data Collection — Expand arXiv Dataset (Target: N=3,000)
- **Current state:** Only 46 papers with metadata. Need ~3,000.
- **Action:** Query arXiv API for papers submitted 7–18 months ago across 7 CS categories
- **Enrichment:** Query Semantic Scholar for each paper's citation count & author h-index
- **Target construction:** `y_paper = normalized(log(1 + citations_180d))` ∈ [0,1]

### Step 3: Data Collection — Construct GitHub Training Dataset (Target: N=2,000)
- **Current state:** 8,679 repos with single snapshot. Need historical star velocity.
- **Action:** Use GitHub Stargazers API to reconstruct star counts at t₀ = Today-30d
- **Target construction:** `y_repo = normalized(log(1 + ΔS_30d))` ∈ [0,1]
- **Fallback:** Use current snapshot features with synthetic velocity proxy

### Step 4: Domain Classification Benchmarking
- Build 500-paper test set (50 per domain) with deterministic arXiv→ATIP domain mapping
- Run `facebook/bart-large-mnli` zero-shot inference
- **Target:** Top-1 Accuracy ≥ 85%, Macro F1 ≥ 0.80
- If below threshold → Fine-tune DistilBERT + ensemble fallback
- Save: `models/domain_classifier_config.json`, `ml_reports/classification_eval_2026_10.json`

### Step 5: Feature Engineering Pipeline
- Create `backend/app/ml/features.py` with `FeatureExtractor` class
- Shared between offline training and online inference (prevents training-serving skew)
- arXiv features: 16 dimensions (text stats + author + category one-hot + domain confidence)
- GitHub features: 20 dimensions (repo stats + license one-hot + language one-hot)

### Step 6: XGBoost Model Training
- **Paper Impact Model:** XGBRegressor on arXiv features → `models/paper_impact_xgb_v1.pkl`
- **Repo Growth Model:** XGBRegressor on GitHub features → `models/repo_growth_xgb_v1.pkl`
- Time-based split (80/20 chronological), 5-fold CV, Ridge baseline comparison
- **Target:** RMSE ≤ 0.20 on normalized [0,1] scale
- TreeSHAP explainability for top-3 feature drivers per prediction

### Step 7: Domain Trend Classifier
- Aggregate daily counts per domain, compute rolling 7d stats
- Binary target: is domain trending (>20% WoW growth)?
- Model: Calibrated LogisticRegression → `models/domain_trend_logreg_v1.pkl`

## 📦 Output Artifacts

| Artifact | Path |
|----------|------|
| Domain classifier config | `models/domain_classifier_config.json` |
| Classification eval report | `ml_reports/classification_eval_2026_10.json` |
| Paper impact XGBoost model | `models/paper_impact_xgb_v1.pkl` |
| Paper feature scaler | `models/paper_feature_scaler_v1.pkl` |
| Repo growth XGBoost model | `models/repo_growth_xgb_v1.pkl` |
| Repo feature scaler | `models/repo_feature_scaler_v1.pkl` |
| Domain trend LogReg model | `models/domain_trend_logreg_v1.pkl` |
| Feature extractor module | `backend/app/ml/features.py` |

## ⚠️ Key Decisions

1. **Cold-start mitigation:** Since we only have single-point snapshots for GitHub repos (not 30-day deltas), we'll construct synthetic velocity targets using star-based proxy metrics for initial training, then retrain as daily snapshots accumulate.

2. **arXiv expansion:** We need to pull ~3,000 historical papers from arXiv API + Semantic Scholar enrichment before training. This is Step 2 and will take ~15-20 minutes.

3. **Classification runs on GPU (Colab):** BART-large-MNLI is too large for local CPU inference at scale. For local development, we'll use the deterministic category→domain mapping as ground truth and benchmark classification accuracy using a saved evaluation script.

## 🚀 Execution Order

```
Step 1 → Install deps & create directories
Step 2 → Collect 3,000 arXiv papers + Semantic Scholar enrichment  
Step 3 → Prepare GitHub training data from existing DB
Step 4 → Classification benchmarking (evaluation script)
Step 5 → Build FeatureExtractor module
Step 6 → Train XGBoost models (Paper Impact + Repo Growth)
Step 7 → Train Domain Trend LogReg
```

> [!TIP]
> Steps 2 & 3 (data collection) can run in parallel. Steps 4, 5, 6, 7 are sequential.
