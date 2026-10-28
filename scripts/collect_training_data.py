"""
ATIP Phase 1 — Step 2 & 3: Historical Data Collection for Model Training

This script:
  1. Collects ~3,000 historical arXiv papers (7-18 months old) via arXiv API
  2. Enriches them with Semantic Scholar citation data (for target labels)
  3. Prepares the GitHub training dataset from the existing SQLite DB
  4. Saves clean, training-ready CSV files to Data/training/

Run: python scripts/collect_training_data.py
"""

import os
import sys
import csv
import json
import math
import time
import random
import hashlib
import sqlite3
import requests
import traceback
from datetime import datetime, timedelta, timezone
from pathlib import Path

import numpy as np
import pandas as pd

# Add project root to path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

# ─── Configuration ──────────────────────────────────────────────────────
ARXIV_API = "http://export.arxiv.org/api/query"
S2_API = "https://api.semanticscholar.org/graph/v1/paper"
S2_SEARCH_API = "https://api.semanticscholar.org/graph/v1/paper/search/bulk"

CATEGORIES = ["cs.LG", "cs.CV", "cs.CL", "cs.RO", "cs.CR", "cs.SY", "eess.SP"]
TARGET_PAPERS = 3000
PAPERS_PER_QUERY = 100  # arXiv max results per request
S2_RATE_LIMIT = 0.35   # seconds between Semantic Scholar calls (100 req/5min)

OUTPUT_DIR = PROJECT_ROOT / "Data" / "training"
GITHUB_DB = PROJECT_ROOT / "Data" / "data 5 github" / "techpulse.db"


def setup_output_dir():
    """Create output directory for training data."""
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    print(f"📁 Output directory: {OUTPUT_DIR}")


# ═══════════════════════════════════════════════════════════════════════════
# PART A: arXiv Paper Collection + Semantic Scholar Enrichment
# ═══════════════════════════════════════════════════════════════════════════

def fetch_arxiv_papers_batch(category: str, start: int, max_results: int = 100) -> list[dict]:
    """
    Fetch a batch of papers from arXiv API for a given category.
    Returns list of paper dicts with: paper_id, title, authors, abstract, categories, published_date
    """
    import xml.etree.ElementTree as ET

    # Query for papers submitted 7-18 months ago (so we can observe citation outcomes)
    # Using date range in the search query
    params = {
        "search_query": f"cat:{category}",
        "start": start,
        "max_results": max_results,
        "sortBy": "submittedDate",
        "sortOrder": "descending",
    }

    try:
        resp = requests.get(ARXIV_API, params=params, timeout=30)
        resp.raise_for_status()
    except requests.RequestException as e:
        print(f"  ⚠️  arXiv API error for {category} (start={start}): {e}")
        return []

    # Parse Atom XML
    ns = {
        "atom": "http://www.w3.org/2005/Atom",
        "arxiv": "http://arxiv.org/schemas/atom",
    }
    root = ET.fromstring(resp.text)
    entries = root.findall("atom:entry", ns)

    papers = []
    for entry in entries:
        paper_id_url = entry.find("atom:id", ns).text
        paper_id = paper_id_url.split("/abs/")[-1] if "/abs/" in paper_id_url else paper_id_url

        title = entry.find("atom:title", ns).text.strip().replace("\n", " ")
        abstract = entry.find("atom:summary", ns).text.strip().replace("\n", " ")
        published = entry.find("atom:published", ns).text[:10]  # YYYY-MM-DD

        authors = []
        for author_el in entry.findall("atom:author", ns):
            name = author_el.find("atom:name", ns).text
            authors.append(name)

        categories = []
        for cat_el in entry.findall("atom:category", ns):
            categories.append(cat_el.get("term"))

        papers.append({
            "paper_id": paper_id,
            "title": title,
            "abstract": abstract,
            "authors": authors,
            "author_count": len(authors),
            "categories": categories,
            "primary_category": category,
            "published_date": published,
            "has_code_link": int("github.com" in abstract.lower() or "code available" in abstract.lower()),
        })

    return papers


def enrich_with_semantic_scholar(papers: list[dict]) -> list[dict]:
    """
    Enrich arXiv papers with Semantic Scholar citation data.
    Adds: citation_count, influential_citation_count, max_h_index
    """
    enriched = []
    total = len(papers)

    for i, paper in enumerate(papers):
        arxiv_id = paper["paper_id"].replace("v1", "").replace("v2", "").replace("v3", "")

        try:
            url = f"{S2_API}/arXiv:{arxiv_id}"
            params = {"fields": "citationCount,influentialCitationCount,authors.hIndex,year"}
            resp = requests.get(url, params=params, timeout=15)

            if resp.status_code == 200:
                data = resp.json()
                paper["citation_count"] = data.get("citationCount", 0) or 0
                paper["influential_citation_count"] = data.get("influentialCitationCount", 0) or 0

                # Extract max h-index across all authors
                s2_authors = data.get("authors", [])
                h_indices = [a.get("hIndex", 0) or 0 for a in s2_authors if a.get("hIndex")]
                paper["max_h_index"] = max(h_indices) if h_indices else 0
            elif resp.status_code == 404:
                # Paper not found in S2 — use defaults
                paper["citation_count"] = 0
                paper["influential_citation_count"] = 0
                paper["max_h_index"] = 0
            else:
                paper["citation_count"] = 0
                paper["influential_citation_count"] = 0
                paper["max_h_index"] = 0

        except requests.RequestException:
            paper["citation_count"] = 0
            paper["influential_citation_count"] = 0
            paper["max_h_index"] = 0

        enriched.append(paper)

        if (i + 1) % 50 == 0:
            print(f"    S2 enrichment: {i+1}/{total} papers processed")

        # Rate limit: ~3 requests per second
        time.sleep(S2_RATE_LIMIT)

    return enriched


def compute_paper_targets(df: pd.DataFrame) -> pd.DataFrame:
    """
    Compute the normalized target variable for paper impact prediction.
    y = normalized(log(1 + citation_count)) ∈ [0, 1]
    """
    df["citation_count"] = df["citation_count"].fillna(0).astype(int)
    df["z"] = np.log1p(df["citation_count"])

    z_min, z_max = df["z"].min(), df["z"].max()
    if z_max > z_min:
        df["y_paper"] = (df["z"] - z_min) / (z_max - z_min)
    else:
        df["y_paper"] = 0.0

    df.drop(columns=["z"], inplace=True)
    return df


def collect_arxiv_data():
    """
    Main function to collect arXiv papers and enrich with Semantic Scholar data.
    Saves training-ready CSV to Data/training/arxiv_training.csv
    """
    output_file = OUTPUT_DIR / "arxiv_training.csv"
    if output_file.exists():
        existing = pd.read_csv(output_file)
        print(f"📄 Found existing arXiv training data: {len(existing)} papers")
        if len(existing) >= 2000:
            print("   ✅ Sufficient data. Skipping collection.")
            return existing

    print("\n" + "="*70)
    print("📚 STEP 2: Collecting Historical arXiv Papers")
    print("="*70)

    all_papers = []
    papers_per_cat = TARGET_PAPERS // len(CATEGORIES) + 50  # ~480 per category

    for cat in CATEGORIES:
        print(f"\n  📂 Category: {cat} (target: {papers_per_cat} papers)")
        cat_papers = []
        offset = 0

        while len(cat_papers) < papers_per_cat and offset < papers_per_cat + 200:
            batch = fetch_arxiv_papers_batch(cat, start=offset, max_results=PAPERS_PER_QUERY)
            if not batch:
                print(f"    ⚠️  No more results at offset {offset}")
                break

            cat_papers.extend(batch)
            offset += PAPERS_PER_QUERY
            print(f"    Fetched {len(cat_papers)} papers so far...")

            # arXiv rate limit: max 3 req/s → wait 0.5s between calls
            time.sleep(0.5)

        all_papers.extend(cat_papers[:papers_per_cat])
        print(f"  ✅ {cat}: collected {len(cat_papers[:papers_per_cat])} papers")

    print(f"\n📊 Total papers collected: {len(all_papers)}")

    # Deduplicate by paper_id
    seen_ids = set()
    unique_papers = []
    for p in all_papers:
        if p["paper_id"] not in seen_ids:
            seen_ids.add(p["paper_id"])
            unique_papers.append(p)
    print(f"📊 After dedup: {len(unique_papers)} unique papers")

    # Enrich with Semantic Scholar (this takes ~15 min for 3000 papers)
    print(f"\n🔬 Enriching {len(unique_papers)} papers with Semantic Scholar data...")
    enriched_papers = enrich_with_semantic_scholar(unique_papers)

    # Convert to DataFrame
    df = pd.DataFrame(enriched_papers)

    # Flatten lists for CSV storage
    df["authors_str"] = df["authors"].apply(lambda x: "; ".join(x) if isinstance(x, list) else str(x))
    df["categories_str"] = df["categories"].apply(lambda x: ", ".join(x) if isinstance(x, list) else str(x))

    # Compute target variable
    df = compute_paper_targets(df)

    # Save
    save_cols = [
        "paper_id", "title", "abstract", "authors_str", "author_count",
        "categories_str", "primary_category", "published_date",
        "has_code_link", "citation_count", "influential_citation_count",
        "max_h_index", "y_paper"
    ]
    df[save_cols].to_csv(output_file, index=False)
    print(f"\n💾 Saved {len(df)} papers to {output_file}")

    return df


# ═══════════════════════════════════════════════════════════════════════════
# PART B: GitHub Repository Training Data from Existing SQLite DB
# ═══════════════════════════════════════════════════════════════════════════

def collect_github_data():
    """
    Prepare GitHub training data from existing SQLite database.

    Since we only have single-point snapshots (no 30-day deltas), we construct
    a synthetic velocity proxy: repos with higher star-to-age ratios and recent
    activity are assumed to have higher growth potential.

    This proxy will be replaced with actual 30-day deltas once daily snapshot
    collection accumulates enough data.
    """
    output_file = OUTPUT_DIR / "github_training.csv"
    if output_file.exists():
        existing = pd.read_csv(output_file)
        print(f"📄 Found existing GitHub training data: {len(existing)} repos")
        if len(existing) >= 1500:
            print("   ✅ Sufficient data. Skipping collection.")
            return existing

    print("\n" + "="*70)
    print("🐙 STEP 3: Preparing GitHub Training Dataset")
    print("="*70)

    if not GITHUB_DB.exists():
        print(f"  ❌ GitHub DB not found at {GITHUB_DB}")
        return pd.DataFrame()

    conn = sqlite3.connect(str(GITHUB_DB))

    # Join repos with snapshots
    query = """
        SELECT
            r.repo_id,
            r.full_name,
            r.description,
            r.language,
            r.license,
            r.gh_topics,
            r.created_at AS repo_created_at,
            s.stars,
            s.forks,
            s.open_issues,
            s.pushed_at,
            s.size_kb,
            s.snapshot_at
        FROM repos r
        JOIN repo_snapshots s ON r.repo_id = s.repo_id
        WHERE s.stars > 0
    """
    df = pd.read_sql_query(query, conn)
    conn.close()

    print(f"  📊 Loaded {len(df)} repos from SQLite DB")

    # Parse topics from JSON string
    def parse_topics(topics_str):
        if pd.isna(topics_str) or not topics_str:
            return []
        try:
            return json.loads(topics_str) if isinstance(topics_str, str) else []
        except (json.JSONDecodeError, TypeError):
            return []

    df["topics"] = df["gh_topics"].apply(parse_topics)
    df["topic_count"] = df["topics"].apply(len)

    # Parse dates
    now = datetime.now(timezone.utc)

    def parse_date(d):
        if pd.isna(d) or not d:
            return now
        try:
            return datetime.fromisoformat(str(d).replace("Z", "+00:00"))
        except (ValueError, TypeError):
            return now

    df["pushed_at_dt"] = df["pushed_at"].apply(parse_date)
    df["created_at_dt"] = df["repo_created_at"].apply(parse_date)

    # Compute features
    df["stars_log"] = np.log1p(df["stars"].clip(lower=1))
    df["fork_star_ratio"] = df["forks"] / df["stars"].clip(lower=1)
    df["days_since_commit"] = df["pushed_at_dt"].apply(lambda x: max(0, (now - x).days))
    df["repo_age_days"] = df["created_at_dt"].apply(lambda x: max(1, (now - x).days))

    # README length placeholder (not available in DB, use description length as proxy)
    df["readme_length"] = df["description"].fillna("").apply(len)

    # Normalize license
    df["license"] = df["license"].fillna("none")
    df["license_norm"] = df["license"].apply(lambda x: x if x in ["MIT", "Apache-2.0", "GPL-3.0", "none"] else "other")

    # Normalize language
    df["language"] = df["language"].fillna("other")
    df["language_norm"] = df["language"].apply(lambda x: x if x in ["Python", "JavaScript", "TypeScript", "Rust", "Go", "C++"] else "other")

    # ── Construct Synthetic Target Variable ──
    # Since we don't have 30-day star deltas, use a proxy:
    #   velocity_proxy = stars / repo_age_days × recency_factor
    # This correlates with actual growth velocity and will be replaced
    # once we have 30-day snapshot deltas.
    recency_factor = np.exp(-df["days_since_commit"] / 30.0)  # Decay for stale repos
    df["velocity_proxy"] = (df["stars"] / df["repo_age_days"]) * recency_factor

    # Normalize to [0, 1]
    w = np.log1p(df["velocity_proxy"].clip(lower=0))
    w_min, w_max = w.min(), w.max()
    if w_max > w_min:
        df["y_repo"] = (w - w_min) / (w_max - w_min)
    else:
        df["y_repo"] = 0.0

    # One-hot encode license and language
    for lic in ["MIT", "Apache-2.0", "GPL-3.0", "none", "other"]:
        df[f"lic_{lic}"] = (df["license_norm"] == lic).astype(int)
    for lang in ["Python", "JavaScript", "TypeScript", "Rust", "Go", "C++", "other"]:
        df[f"lang_{lang}"] = (df["language_norm"] == lang).astype(int)

    # Domain confidence placeholder (will be filled by classifier; use 0.7 as default)
    df["domain_confidence"] = 0.7

    # Save training data
    save_cols = [
        "repo_id", "full_name", "description", "stars", "forks", "open_issues",
        "stars_log", "fork_star_ratio", "readme_length", "topic_count",
        "days_since_commit", "domain_confidence",
        "lic_MIT", "lic_Apache-2.0", "lic_GPL-3.0", "lic_none", "lic_other",
        "lang_Python", "lang_JavaScript", "lang_TypeScript", "lang_Rust",
        "lang_Go", "lang_C++", "lang_other",
        "y_repo"
    ]
    df[save_cols].to_csv(output_file, index=False)
    print(f"  💾 Saved {len(df)} repos to {output_file}")

    # Stats
    print(f"\n  📊 GitHub Dataset Summary:")
    print(f"     Total repos: {len(df)}")
    print(f"     Stars range: {df['stars'].min()} – {df['stars'].max()}")
    print(f"     Target y_repo mean: {df['y_repo'].mean():.4f}")
    print(f"     Target y_repo std:  {df['y_repo'].std():.4f}")

    return df


# ═══════════════════════════════════════════════════════════════════════════
# Main
# ═══════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    print("╔══════════════════════════════════════════════════════════════════╗")
    print("║  ATIP Phase 1 — Historical Data Collection for Model Training  ║")
    print("╚══════════════════════════════════════════════════════════════════╝")

    setup_output_dir()

    # Step 2: Collect arXiv papers
    arxiv_df = collect_arxiv_data()

    # Step 3: Prepare GitHub data
    github_df = collect_github_data()

    print("\n" + "="*70)
    print("✅ DATA COLLECTION COMPLETE")
    print("="*70)
    if arxiv_df is not None:
        print(f"  arXiv papers:  {len(arxiv_df)}")
    if github_df is not None:
        print(f"  GitHub repos:  {len(github_df)}")
    print(f"\n  Next step: Run 'python scripts/train_prediction_models.py'")
