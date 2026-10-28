"""
Automated Pytest Suite for Review System Web Application
Tests cover:
- Home page availability and template rendering
- Health check endpoint response and schema
- Version configuration validation
- Valid review submission and redirect handling
- Input validation and rejection of invalid reviews
- Review list rendering and content display
- Filter and statistics calculation logic
"""

import pytest
import app as app_module


@pytest.fixture
def client():
    """Create a fresh test client with test configuration."""
    app_module.app.config["TESTING"] = True
    # Save a backup of initial reviews to maintain test isolation
    initial_reviews_backup = [dict(r) for r in app_module.reviews]

    with app_module.app.test_client() as test_client:
        yield test_client

    # Restore initial reviews state after test
    app_module.reviews.clear()
    app_module.reviews.extend(initial_reviews_backup)


def test_home_page_returns_200(client):
    """Verify home page loads successfully with HTTP 200."""
    response = client.get("/")
    assert response.status_code == 200
    assert b"Review System" in response.data
    assert b"Submit a Review" in response.data


def test_health_endpoint_is_healthy(client):
    """Verify /health endpoint returns HTTP 200 and healthy status."""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.get_json()
    assert data is not None
    assert data.get("status") == "healthy"


def test_health_endpoint_includes_version(client):
    """Verify /health endpoint reports the configured application version."""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.get_json()
    assert "version" in data
    assert data["version"] == app_module.APP_VERSION


def test_submit_valid_review_redirects_and_saves(client):
    """Verify valid review submission redirects with 302 and appears in list."""
    payload = {
        "name": "Priya Sharma",
        "rating": "5",
        "comment": "Exceptional customer service and quick resolution!",
    }
    response = client.post("/reviews", data=payload)
    assert response.status_code == 302
    assert response.headers["Location"].endswith("/")

    # Follow redirect to verify review is rendered
    follow_response = client.get("/")
    assert follow_response.status_code == 200
    assert b"Priya Sharma" in follow_response.data
    assert b"Exceptional customer service" in follow_response.data


def test_invalid_review_missing_name_rejected(client):
    """Verify review with empty name is rejected with HTTP 400."""
    payload = {
        "name": "",
        "rating": "5",
        "comment": "Good product but name is missing",
    }
    response = client.post("/reviews", data=payload)
    assert response.status_code == 400
    assert b"Name is required" in response.data


def test_invalid_review_missing_comment_rejected(client):
    """Verify review with empty comment is rejected with HTTP 400."""
    payload = {
        "name": "John Doe",
        "rating": "4",
        "comment": "",
    }
    response = client.post("/reviews", data=payload)
    assert response.status_code == 400
    assert b"Comment is required" in response.data


def test_invalid_review_out_of_range_rating_rejected(client):
    """Verify review with rating outside 1-5 range is rejected with HTTP 400."""
    for bad_rating in ["0", "6", "99", "-1", "abc"]:
        payload = {
            "name": "Jane Doe",
            "rating": bad_rating,
            "comment": "Testing invalid rating boundary",
        }
        response = client.post("/reviews", data=payload)
        assert response.status_code == 400
        assert b"Rating must be an integer between 1 and 5" in response.data


def test_reviews_page_returns_200(client):
    """Verify dedicated /reviews page loads with HTTP 200 and displays reviews."""
    response = client.get("/reviews")
    assert response.status_code == 200
    assert b"All Customer Reviews" in response.data
    assert b"Aarav Sharma" in response.data


def test_statistics_calculation_accuracy():
    """Verify calculation of aggregates, averages, and distribution."""
    sample_data = [
        {"rating": 5},
        {"rating": 5},
        {"rating": 4},
        {"rating": 2},
    ]
    stats = app_module.calculate_statistics(sample_data)
    assert stats["total"] == 4
    # (5 + 5 + 4 + 2) / 4 = 16 / 4 = 4.0
    assert stats["avg_rating"] == 4.0
    assert stats["five_star_count"] == 2
    # 3 out of 4 are >= 4 stars -> 75%
    assert stats["positive_pct"] == 75.0
    assert stats["distribution"][5] == 2
    assert stats["distribution"][4] == 1
    assert stats["distribution"][2] == 1
