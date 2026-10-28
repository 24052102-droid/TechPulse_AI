import pytest


def test_root_endpoint(client):
    """Verifies that the root API welcome endpoint responds."""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "platform" in data
    assert data["status"] == "online"


def test_health_endpoints(client):
    """Verifies both /health and /api/health routes function correctly."""
    for path in ["/health", "/api/health"]:
        response = client.get(path)
        assert response.status_code == 200
        data = response.json()
        assert data["status"] in ["healthy", "degraded"]
        assert "database" in data
        assert "cache" in data


def test_feed_dual_routing(client):
    """Verifies /feed and /api/feed both return 200 OK."""
    for path in ["/feed", "/api/feed"]:
        response = client.get(path)
        assert response.status_code == 200
        data = response.json()
        assert "items" in data
        assert "total" in data


def test_trends_dual_routing(client):
    """Verifies /trends and /api/trends both return 200 OK."""
    for path in ["/trends", "/api/trends"]:
        response = client.get(path)
        assert response.status_code == 200
        data = response.json()
        assert "domains" in data or isinstance(data, dict)


def test_domains_dual_routing(client):
    """Verifies /domains and /api/domains both return 200 OK."""
    for path in ["/domains", "/api/domains"]:
        response = client.get(path)
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, (list, dict))


def test_search_endpoint(client):
    """Verifies search endpoint handles queries gracefully."""
    response = client.get("/api/search?q=neural")
    assert response.status_code == 200
    data = response.json()
    assert "query" in data
    assert "results" in data


def test_evaluation_metrics(client):
    """Verifies model scorecard metrics endpoint returns valid data."""
    response = client.get("/api/evaluation")
    assert response.status_code == 200
    data = response.json()
    assert "paper_impact_model" in data or "models" in data or "phase" in data

