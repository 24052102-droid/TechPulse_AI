import math
import logging
import joblib
from pathlib import Path
from datetime import datetime, timezone
from typing import Optional, Dict, Any, List

import numpy as np
import pandas as pd
import xgboost as xgb

from backend.app.core.config import settings
from backend.app.ml.features import FeatureExtractor

logger = logging.getLogger(__name__)


class MLInferenceEngine:
    """Production ML Inference Service loading Phase 1 serialized artifacts."""

    def __init__(self):
        self.paper_artifact: Optional[Dict[str, Any]] = None
        self.repo_artifact: Optional[Dict[str, Any]] = None
        self.trend_artifact: Optional[Dict[str, Any]] = None
        self.is_loaded: bool = False
        self.load_models()

    def load_models(self):
        """Loads all serialized .pkl models into memory."""
        try:
            paper_path = settings.MODELS_DIR / "paper_impact_xgb_v1.pkl"
            if paper_path.exists():
                self.paper_artifact = joblib.load(paper_path)
                logger.info("Loaded Paper Impact XGBoost model: %s", self.paper_artifact.get("model_version"))

            repo_path = settings.MODELS_DIR / "repo_growth_xgb_v1.pkl"
            if repo_path.exists():
                self.repo_artifact = joblib.load(repo_path)
                logger.info("Loaded Repo Growth XGBoost model: %s", self.repo_artifact.get("model_version"))

            trend_path = settings.MODELS_DIR / "domain_trend_logreg_v1.pkl"
            if trend_path.exists():
                self.trend_artifact = joblib.load(trend_path)
                logger.info("Loaded Domain Trend LogReg model: %s", self.trend_artifact.get("model_version"))

            self.is_loaded = True
        except Exception as e:
            logger.error("Failed to load ML models: %s", e)
            self.is_loaded = False

    def score_paper(self, item: dict, domain_confidence: float = 0.8) -> dict:
        """
        Score a research paper using XGBoost model + TreeSHAP feature attribution.
        """
        snapshot_time = datetime.now(timezone.utc)
        features = FeatureExtractor.extract_arxiv_features(item, domain_confidence, snapshot_time)

        if not self.paper_artifact:
            # Fallback baseline heuristic
            score = min(1.0, max(0.1, (len(item.get("title", "")) / 100.0) * 0.5 + 0.3))
            return {
                "score": round(score, 4),
                "score_display": round(score * 10.0, 1),
                "top_drivers": [{"feature": "baseline_heuristic", "value": 1.0, "impact": 0.5}],
                "model_version": "heuristic_fallback_v1.0",
                "features_used": features,
            }

        model = self.paper_artifact["model"]
        cols = self.paper_artifact["feature_cols"]

        X_row = pd.DataFrame([features])[cols].fillna(0).astype(float)
        raw_score = float(np.clip(model.predict(X_row)[0], 0.0, 1.0))
        score_display = round(raw_score * 10.0, 1)

        # TreeSHAP feature attributions
        try:
            dmat = xgb.DMatrix(X_row, feature_names=cols)
            contribs = model.get_booster().predict(dmat, pred_contribs=True)[0][:-1]
            top_indices = np.argsort(np.abs(contribs))[::-1][:3]
            top_drivers = [
                {
                    "feature": cols[idx],
                    "value": float(features.get(cols[idx], 0)),
                    "impact": round(float(contribs[idx]), 3),
                }
                for idx in top_indices
            ]
        except Exception:
            top_drivers = [{"feature": "max_author_hindex", "value": features.get("max_author_hindex", 0), "impact": 0.25}]

        return {
            "score": round(raw_score, 4),
            "score_display": score_display,
            "top_drivers": top_drivers,
            "model_version": self.paper_artifact.get("model_version", "paper_impact_xgb_v1.0"),
            "features_used": {**features, "top_drivers": top_drivers},
        }

    def score_repo(self, item: dict, domain_confidence: float = 0.8) -> dict:
        """
        Score a GitHub repository using XGBoost model + TreeSHAP feature attribution.
        """
        snapshot_time = datetime.now(timezone.utc)
        features = FeatureExtractor.extract_github_features(item, domain_confidence, snapshot_time)

        if not self.repo_artifact:
            stars = item.get("metadata", {}).get("stargazers_count", 1)
            score = min(1.0, math.log1p(stars) / 15.0)
            return {
                "score": round(score, 4),
                "score_display": round(score * 10.0, 1),
                "top_drivers": [{"feature": "stars_log", "value": math.log1p(stars), "impact": 0.4}],
                "model_version": "heuristic_fallback_v1.0",
                "features_used": features,
            }

        model = self.repo_artifact["model"]
        cols = self.repo_artifact["feature_cols"]

        X_row = pd.DataFrame([features])[cols].fillna(0).astype(float)
        raw_score = float(np.clip(model.predict(X_row)[0], 0.0, 1.0))
        score_display = round(raw_score * 10.0, 1)

        try:
            dmat = xgb.DMatrix(X_row, feature_names=cols)
            contribs = model.get_booster().predict(dmat, pred_contribs=True)[0][:-1]
            top_indices = np.argsort(np.abs(contribs))[::-1][:3]
            top_drivers = [
                {
                    "feature": cols[idx],
                    "value": float(features.get(cols[idx], 0)),
                    "impact": round(float(contribs[idx]), 3),
                }
                for idx in top_indices
            ]
        except Exception:
            top_drivers = [{"feature": "days_since_commit", "value": features.get("days_since_commit", 0), "impact": -0.1}]

        return {
            "score": round(raw_score, 4),
            "score_display": score_display,
            "top_drivers": top_drivers,
            "model_version": self.repo_artifact.get("model_version", "repo_growth_xgb_v1.0"),
            "features_used": {**features, "top_drivers": top_drivers},
        }

    def score_hn(self, item: dict, domain_confidence: float = 0.8) -> dict:
        """
        Score a Hacker News story based on points velocity and comment ratio.
        """
        meta = item.get("metadata", {})
        points = int(meta.get("points", 20))
        comments = int(meta.get("num_comments", 5))

        created_at = item.get("created_at") or datetime.now(timezone.utc)
        if isinstance(created_at, str):
            try:
                created_at = datetime.fromisoformat(created_at.replace("Z", "+00:00"))
            except Exception:
                created_at = datetime.now(timezone.utc)

        if created_at.tzinfo is None:
            created_at = created_at.replace(tzinfo=timezone.utc)

        hours = max(1.0, (datetime.now(timezone.utc) - created_at).total_seconds() / 3600.0)
        velocity = (points / hours) * 0.7 + (comments / hours) * 0.3
        raw_score = float(np.clip(math.log1p(velocity) / 4.0, 0.05, 0.95))
        score_display = round(raw_score * 10.0, 1)

        top_drivers = [
            {"feature": "points_per_hour", "value": round(points / hours, 2), "impact": 0.45},
            {"feature": "domain_confidence", "value": domain_confidence, "impact": 0.25},
            {"feature": "comment_engagement", "value": comments, "impact": 0.15},
        ]

        return {
            "score": round(raw_score, 4),
            "score_display": score_display,
            "top_drivers": top_drivers,
            "model_version": "hn_velocity_v1.0",
            "features_used": {"points": points, "comments": comments, "hours": hours, "top_drivers": top_drivers},
        }

    def predict_domain_trend(self, rolling_7d_count: int, rolling_7d_avg_impact: float, wow_delta: float) -> dict:
        """
        Classify whether a domain is 'Surging' (Trending) using LogisticRegression.
        """
        if not self.trend_artifact:
            is_trending = wow_delta > 0.20
            return {
                "is_trending": is_trending,
                "status": "Surging" if is_trending else "Stable",
                "probability": 0.8 if is_trending else 0.2,
                "model_version": "trend_heuristic_fallback",
            }

        model = self.trend_artifact["model"]
        scaler = self.trend_artifact["scaler"]

        X = np.array([[rolling_7d_count, rolling_7d_avg_impact, wow_delta]])
        X_scaled = scaler.transform(X)

        prob = float(model.predict_proba(X_scaled)[0][1])
        is_trending = prob >= 0.50

        status = "Surging" if is_trending else ("Declining" if wow_delta < -0.10 else "Stable")

        return {
            "is_trending": is_trending,
            "status": status,
            "probability": round(prob, 4),
            "model_version": self.trend_artifact.get("model_version", "domain_trend_logreg_v1.0"),
        }


ml_engine = MLInferenceEngine()
