"""
ATIP Phase 1 — Fast Historical arXiv Collection & Semantic Scholar Batch Enrichment

This script:
  1. Queries arXiv API for historical papers submitted 7-18 months ago across 7 categories:
     cs.LG, cs.CV, cs.CL, cs.RO, cs.CR, cs.SY, eess.SP
  2. Uses Semantic Scholar POST /graph/v1/paper/batch (100 papers per call)
     to enrich with real 180-day citation counts and author h-indices in seconds.
  3. Pre-computes normalized y_paper targets.
  4. Saves clean training CSV to Data/training/arxiv_training.csv.
"""

import os
import sys
import time
import math
import requests
import xml.etree.ElementTree as ET
from pathlib import Path
from datetime import datetime, timezone
import pandas as pd
import numpy as np

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from backend.app.ml.features import (
    FeatureExtractor,
    ARXIV_CATEGORIES,
    CATEGORY_TO_DOMAIN,
)

OUTPUT_DIR = PROJECT_ROOT / "Data" / "training"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
OUTPUT_FILE = OUTPUT_DIR / "arxiv_training.csv"

# Historical date range: 7 to 18 months ago
# e.g., May 1, 2023 to April 30, 2024
DATE_FILTER = "submittedDate:[202305010000 TO 202404302359]"
PAPERS_PER_CAT = 300
BATCH_SIZE = 100


def fetch_arxiv_category(category: str, target_count: int = 300) -> list[dict]:
    """Fetch historical papers from arXiv for a specific category."""
    print(f"  Fetching arXiv historical papers for {category} (target: {target_count})...")
    ns = {"atom": "http://www.w3.org/2005/Atom"}
    papers = []
    start = 0

    while len(papers) < target_count and start < target_count + 150:
        fetch_n = min(BATCH_SIZE, target_count - len(papers))
        params = {
            "search_query": f"cat:{category} AND {DATE_FILTER}",
            "start": start,
            "max_results": fetch_n,
            "sortBy": "submittedDate",
            "sortOrder": "descending",
        }
        try:
            resp = requests.get("http://export.arxiv.org/api/query", params=params, timeout=25)
            if resp.status_code != 200:
                print(f"    arXiv returned {resp.status_code} for {category} start={start}")
                break

            root = ET.fromstring(resp.text)
            entries = root.findall("atom:entry", ns)
            if not entries:
                print(f"    No more entries for {category} at offset {start}")
                break

            for entry in entries:
                paper_id_url = entry.find("atom:id", ns).text
                raw_id = paper_id_url.split("/abs/")[-1] if "/abs/" in paper_id_url else paper_id_url
                clean_id = raw_id.split("v")[0]

                title = entry.find("atom:title", ns).text.strip().replace("\n", " ")
                summary_el = entry.find("atom:summary", ns)
                abstract = summary_el.text.strip().replace("\n", " ") if summary_el is not None else ""
                published = entry.find("atom:published", ns).text[:10]

                authors = [a.find("atom:name", ns).text for a in entry.findall("atom:author", ns)]
                cats = [c.get("term") for c in entry.findall("atom:category", ns)]

                has_code = int("github.com" in abstract.lower() or "code available" in abstract.lower())

                papers.append({
                    "paper_id": clean_id,
                    "title": title,
                    "abstract": abstract,
                    "authors": authors,
                    "author_count": len(authors),
                    "categories": cats,
                    "primary_category": category,
                    "published_date": published,
                    "has_code_link": has_code,
                })

            start += len(entries)
            print(f"    {category}: {len(papers)} papers collected (start={start})")
            time.sleep(1.2)  # Respect arXiv API rate limit

        except Exception as e:
            print(f"    Error fetching {category} at {start}: {e}")
            break

    return papers


def enrich_with_s2_batch(papers: list[dict]) -> list[dict]:
    """Enrich papers with Semantic Scholar batch API in chunks of 100."""
    print(f"\n🔬 Enriching {len(papers)} papers using Semantic Scholar Batch API...")
    url = "https://api.semanticscholar.org/graph/v1/paper/batch?fields=citationCount,influentialCitationCount,authors.hIndex"
    
    chunk_size = 100
    enriched_map = {}

    for i in range(0, len(papers), chunk_size):
        chunk = papers[i:i + chunk_size]
        ids = [f"arXiv:{p['paper_id']}" for p in chunk]
        
        try:
            resp = requests.post(url, json={"ids": ids}, timeout=20)
            if resp.status_code == 200:
                data = resp.json()
                for p_obj, orig in zip(data, chunk):
                    if p_obj:
                        c_count = p_obj.get("citationCount", 0) or 0
                        inf_count = p_obj.get("influentialCitationCount", 0) or 0
                        authors = p_obj.get("authors", []) or []
                        h_indices = [a.get("hIndex", 0) or 0 for a in authors if a and a.get("hIndex")]
                        max_h = max(h_indices) if h_indices else 0
                        enriched_map[orig["paper_id"]] = {
                            "citation_count": c_count,
                            "influential_citation_count": inf_count,
                            "max_h_index": max_h,
                        }
                    else:
                        enriched_map[orig["paper_id"]] = {
                            "citation_count": 0,
                            "influential_citation_count": 0,
                            "max_h_index": 0,
                        }
            else:
                print(f"    S2 batch returned {resp.status_code} for chunk {i//chunk_size + 1}")
        except Exception as e:
            print(f"    S2 batch error on chunk {i//chunk_size + 1}: {e}")

        done = min(i + chunk_size, len(papers))
        print(f"    Enriched {done}/{len(papers)} papers...")
        time.sleep(1.5)  # Rate limit courtesy for S2

    for p in papers:
        s2_info = enriched_map.get(p["paper_id"], {"citation_count": 0, "influential_citation_count": 0, "max_h_index": 0})
        p.update(s2_info)

    return papers


def main():
    print("=" * 70)
    print("ATIP Phase 1: Historical arXiv Collection + Batch Enrichment")
    print("=" * 70)

    all_papers = []
    for cat in ARXIV_CATEGORIES:
        cat_papers = fetch_arxiv_category(cat, target_count=PAPERS_PER_CAT)
        all_papers.extend(cat_papers)
        print(f"  --> Total so far: {len(all_papers)} papers")

    # Deduplicate
    seen = set()
    unique_papers = []
    for p in all_papers:
        if p["paper_id"] not in seen:
            seen.add(p["paper_id"])
            unique_papers.append(p)

    print(f"\nTotal unique papers after dedup: {len(unique_papers)}")

    # Batch enrich
    enriched_papers = enrich_with_s2_batch(unique_papers)

    df = pd.DataFrame(enriched_papers)
    df["authors_str"] = df["authors"].apply(lambda x: "; ".join(x) if isinstance(x, list) else str(x))
    df["categories_str"] = df["categories"].apply(lambda x: ", ".join(x) if isinstance(x, list) else str(x))

    # Compute target y_paper
    df["citation_count"] = df["citation_count"].fillna(0).astype(int)
    z = np.log1p(df["citation_count"])
    z_min, z_max = z.min(), z.max()
    df["y_paper"] = (z - z_min) / (z_max - z_min) if z_max > z_min else 0.0

    save_cols = [
        "paper_id", "title", "abstract", "authors_str", "author_count",
        "categories_str", "primary_category", "published_date", "has_code_link",
        "citation_count", "influential_citation_count", "max_h_index", "y_paper",
    ]
    df[save_cols].to_csv(OUTPUT_FILE, index=False)

    print(f"\n SUCCESS! Saved {len(df)} historical papers to {OUTPUT_FILE}")
    print(f"Citations summary:\n{df['citation_count'].describe()}")
    print(f"y_paper summary:\n{df['y_paper'].describe()}")


if __name__ == "__main__":
    main()
