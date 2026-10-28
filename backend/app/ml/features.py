"""
FeatureExtractor — Shared feature engineering module for ATIP/TechPulse AI.

This module is used identically during:
  1. Offline model training (scripts/train_prediction_models.py)
  2. Online Celery inference (backend/app/tasks/predict.py)

Keeping a single source of truth prevents training-serving skew.
"""

import math
from datetime import datetime, timezone
from typing import Optional

try:
    import textstat
except ImportError:
    textstat = None  # Graceful fallback for environments without textstat


# ─── Constants ──────────────────────────────────────────────────────────
ARXIV_CATEGORIES = ["cs.LG", "cs.CV", "cs.CL", "cs.RO", "cs.CR", "cs.SY", "eess.SP"]
LICENSES = ["MIT", "Apache-2.0", "GPL-3.0", "none", "other"]
LANGUAGES = ["Python", "JavaScript", "TypeScript", "Rust", "Go", "C++", "other"]

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
    "Multimodal and Foundation Models",
]

# Deterministic mapping: arXiv category → ATIP domain label (ground truth for eval)
CATEGORY_TO_DOMAIN = {
    "cs.CL": "Natural Language Processing",
    "cs.CV": "Computer Vision",
    "cs.RO": "Robotics",
    "cs.CR": "Security and Privacy",
    "cs.SY": "Systems and Infrastructure",
    "cs.DC": "Systems and Infrastructure",
    "cs.OS": "Systems and Infrastructure",
    "eess.SP": "IoT and Embedded Systems",
    "cs.AR": "IoT and Embedded Systems",
    "cs.DB": "Data Engineering and Pipelines",
    "cs.LG": "General Machine Learning",
    "stat.ML": "General Machine Learning",
}


class FeatureExtractor:
    """Deterministic, reusable feature extraction for both arXiv papers and GitHub repos."""

    @staticmethod
    def extract_arxiv_features(
        item: dict,
        classification_score: float,
        snapshot_time: Optional[datetime] = None,
    ) -> dict:
        """
        Extract ML features for an arXiv paper item.

        Args:
            item: dict with keys: title, description (abstract), metadata (authors, categories, etc.), created_at
            classification_score: confidence score from the domain classifier
            snapshot_time: reference time for computing 'days_since_submission'

        Returns:
            dict of feature_name → feature_value (16 dimensions total)
        """
        if snapshot_time is None:
            snapshot_time = datetime.now(timezone.utc)

        title = item.get("title", "")
        abstract = item.get("description", "") or item.get("abstract", "")
        meta = item.get("metadata", {})
        authors = meta.get("authors", [])
        categories = meta.get("categories", [])

        # Handle categories as a string (comma/space separated) or list
        if isinstance(categories, str):
            categories = [c.strip() for c in categories.replace(",", " ").split()]

        created_at = item.get("created_at") or snapshot_time
        if isinstance(created_at, str):
            try:
                created_at = datetime.fromisoformat(created_at.replace("Z", "+00:00"))
            except (ValueError, TypeError):
                created_at = snapshot_time

        if created_at.tzinfo is None:
            created_at = created_at.replace(tzinfo=timezone.utc)
        if snapshot_time.tzinfo is None:
            snapshot_time = snapshot_time.replace(tzinfo=timezone.utc)

        days_since_sub = max(0, (snapshot_time - created_at).days)

        # Compute Flesch readability if textstat is available
        flesch = 50.0
        if textstat and abstract:
            try:
                flesch = textstat.flesch_reading_ease(abstract)
            except Exception:
                flesch = 50.0

        features = {
            "title_word_count": len(title.split()),
            "abstract_word_count": len(abstract.split()),
            "flesch_score": flesch,
            "domain_confidence": float(classification_score),
            "author_count": len(authors) if isinstance(authors, list) else 1,
            "max_author_hindex": float(meta.get("max_h_index", 0)),
            "days_since_submission": days_since_sub,
            "has_code_link": int(
                "github.com" in abstract.lower() or "code available" in abstract.lower()
            ),
            "num_figures": int(meta.get("num_figures", 0)),
        }

        # One-hot encode 7 arXiv categories
        for cat in ARXIV_CATEGORIES:
            features[f"cat_{cat}"] = int(cat in categories)

        return features

    @staticmethod
    def extract_github_features(
        item: dict,
        classification_score: float,
        snapshot_time: Optional[datetime] = None,
    ) -> dict:
        """
        Extract ML features for a GitHub repository item.

        Args:
            item: dict with keys: title, description, metadata (stars, forks, topics, etc.)
            classification_score: confidence score from the domain classifier
            snapshot_time: reference time for computing 'days_since_commit'

        Returns:
            dict of feature_name → feature_value (20 dimensions total)
        """
        if snapshot_time is None:
            snapshot_time = datetime.now(timezone.utc)

        meta = item.get("metadata", {})
        stars = max(int(meta.get("stargazers_count", meta.get("stars", 1))), 1)
        forks = int(meta.get("forks_count", meta.get("forks", 0)))

        pushed_at = meta.get("pushed_at")
        if isinstance(pushed_at, str):
            try:
                pushed_at = datetime.fromisoformat(pushed_at.replace("Z", "+00:00"))
            except (ValueError, TypeError):
                pushed_at = snapshot_time
        elif not isinstance(pushed_at, datetime):
            pushed_at = snapshot_time

        if pushed_at.tzinfo is None:
            pushed_at = pushed_at.replace(tzinfo=timezone.utc)
        if snapshot_time.tzinfo is None:
            snapshot_time = snapshot_time.replace(tzinfo=timezone.utc)

        days_since_commit = max(0, (snapshot_time - pushed_at).days)

        # Normalize license
        lic = meta.get("license") or "none"
        lic_norm = lic if lic in LICENSES else "other"

        # Normalize language
        lang = meta.get("language") or "other"
        lang_norm = lang if lang in LANGUAGES else "other"

        features = {
            "stars_log": math.log1p(stars),
            "forks": forks,
            "fork_star_ratio": round(forks / stars, 4),
            "open_issues": int(meta.get("open_issues_count", meta.get("open_issues", 0))),
            "readme_length": len(meta.get("readme_snippet", "")),
            "topic_count": len(meta.get("topics", [])),
            "days_since_commit": days_since_commit,
            "domain_confidence": float(classification_score),
        }

        # One-hot encode license types
        for l_val in LICENSES:
            features[f"lic_{l_val}"] = int(lic_norm == l_val)

        # One-hot encode language types
        for lg_val in LANGUAGES:
            features[f"lang_{lg_val}"] = int(lang_norm == lg_val)

        return features

    @staticmethod
    def get_arxiv_feature_columns() -> list[str]:
        """Returns the ordered list of feature column names for arXiv models."""
        base = [
            "title_word_count",
            "abstract_word_count",
            "flesch_score",
            "domain_confidence",
            "author_count",
            "max_author_hindex",
            "days_since_submission",
            "has_code_link",
            "num_figures",
        ]
        cat_cols = [f"cat_{cat}" for cat in ARXIV_CATEGORIES]
        return base + cat_cols

    @staticmethod
    def get_github_feature_columns() -> list[str]:
        """Returns the ordered list of feature column names for GitHub models."""
        base = [
            "stars_log",
            "forks",
            "fork_star_ratio",
            "open_issues",
            "readme_length",
            "topic_count",
            "days_since_commit",
            "domain_confidence",
        ]
        lic_cols = [f"lic_{l}" for l in LICENSES]
        lang_cols = [f"lang_{lg}" for lg in LANGUAGES]
        return base + lic_cols + lang_cols
