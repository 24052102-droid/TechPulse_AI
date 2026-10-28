import pytest
from backend.app.ml.inference import ml_engine


def test_ml_models_loaded():
    """Ensures all 3 serialized Phase 1 model artifacts exist and loaded."""
    assert ml_engine.is_loaded is True
    assert ml_engine.paper_artifact is not None
    assert ml_engine.repo_artifact is not None
    assert ml_engine.trend_artifact is not None


def test_paper_impact_prediction():
    """Verifies paper impact prediction returns valid score and SHAP drivers."""
    mock_paper = {
        "title": "Attention Is All You Need for Multimodal Agents",
        "description": "We present a novel transformer architecture with code repository.",
        "primary_category": "cs.LG",
        "created_at": "2024-01-15T00:00:00Z",
        "metadata": {
            "authors": ["Ashish Vaswani", "Noam Shazeer"],
            "max_author_hindex": 45,
            "mean_author_hindex": 30.5,
            "citation_count": 250,
            "repo_url": "https://github.com/google/transformer",
        },
    }
    result = ml_engine.score_paper(mock_paper, domain_confidence=0.85)
    assert "score" in result
    assert "score_display" in result
    assert 0.0 <= result["score_display"] <= 10.0
    assert "top_drivers" in result
    assert isinstance(result["top_drivers"], list)
    assert len(result["top_drivers"]) <= 3


def test_repo_growth_prediction():
    """Verifies repo growth prediction returns valid score and SHAP drivers."""
    mock_repo = {
        "title": "vllm-project/vllm",
        "description": "A high-throughput and memory-efficient inference and serving engine for LLMs",
        "created_at": "2023-06-01T00:00:00Z",
        "metadata": {
            "stargazers_count": 25000,
            "forks_count": 3500,
            "open_issues_count": 120,
            "language": "Python",
            "license": "Apache-2.0",
            "pushed_at": "2024-01-15T00:00:00Z",
        },
    }
    result = ml_engine.score_repo(mock_repo, domain_confidence=0.90)
    assert "score" in result
    assert "score_display" in result
    assert 0.0 <= result["score_display"] <= 10.0
    assert "top_drivers" in result
    assert isinstance(result["top_drivers"], list)
    assert len(result["top_drivers"]) <= 3
