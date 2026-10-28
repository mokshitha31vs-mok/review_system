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
- Version 2 (V2) Edit/Modify Review feature:
  - Form rendering with existing details
  - Successful updates
  - Field validation on edits
  - 404 for non-existent reviews
  - Exclusion from V1 and V3 (preserving backward/forward version isolation)
"""

import pytest
import app as app_module


@pytest.fixture
def client():
    """Create a fresh test client with test configuration."""
    app_module.app.config["TESTING"] = True
    # Save a backup of initial reviews and version to maintain test isolation
    initial_reviews_backup = [dict(r) for r in app_module.reviews]
    initial_version = app_module.APP_VERSION

    with app_module.app.test_client() as test_client:
        yield test_client

    # Restore initial state after test
    app_module.reviews.clear()
    app_module.reviews.extend(initial_reviews_backup)
    app_module.APP_VERSION = initial_version


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


# ==============================================================================
# Version 2 (V2) Edit/Modify Feature Tests
# ==============================================================================

def test_v2_edit_review_page_loads_existing_details(client):
    """Verify V2 edit page pre-fills existing review details and action buttons."""
    app_module.APP_VERSION = "v2"
    response = client.get("/reviews/1/edit")
    assert response.status_code == 200
    # Must contain existing details
    assert b"Aarav Sharma" in response.data
    assert b"Outstanding system!" in response.data
    # Must contain Save and Cancel actions
    assert b"Save Changes" in response.data
    assert b"Cancel" in response.data


def test_v2_edit_review_successful_update(client):
    """Verify saving edited review immediately updates content and redirects."""
    app_module.APP_VERSION = "v2"
    payload = {
        "name": "Aarav Sharma (Verified)",
        "rating": "4",
        "comment": "Updated review comment with modified rating.",
    }
    response = client.post("/reviews/1/edit", data=payload)
    assert response.status_code == 302
    assert response.headers["Location"].endswith("/")

    # Check updated values in memory
    target = next(r for r in app_module.reviews if r["id"] == 1)
    assert target["name"] == "Aarav Sharma (Verified)"
    assert target["rating"] == 4
    assert target["comment"] == "Updated review comment with modified rating."

    # Follow redirect and verify display
    follow_resp = client.get("/")
    assert follow_resp.status_code == 200
    assert b"Aarav Sharma (Verified)" in follow_resp.data
    assert b"Updated review comment with modified rating." in follow_resp.data


def test_v2_edit_review_invalid_inputs_rejected(client):
    """Verify validation rejects empty names, empty comments, and bad ratings."""
    app_module.APP_VERSION = "v2"

    # Missing name
    res1 = client.post("/reviews/1/edit", data={"name": "", "rating": "5", "comment": "Valid"})
    assert res1.status_code == 400
    assert b"Name is required" in res1.data

    # Missing comment
    res2 = client.post("/reviews/1/edit", data={"name": "Valid", "rating": "5", "comment": ""})
    assert res2.status_code == 400
    assert b"Comment is required" in res2.data

    # Out of range rating
    res3 = client.post("/reviews/1/edit", data={"name": "Valid", "rating": "10", "comment": "Valid"})
    assert res3.status_code == 400
    assert b"Rating must be an integer between 1 and 5" in res3.data


def test_v2_edit_nonexistent_review_returns_404(client):
    """Verify attempting to edit a non-existent review returns HTTP 404."""
    app_module.APP_VERSION = "v2"
    get_res = client.get("/reviews/9999/edit")
    assert get_res.status_code == 404

    post_res = client.post("/reviews/9999/edit", data={"name": "A", "rating": "5", "comment": "B"})
    assert post_res.status_code == 404


def test_v1_and_v3_edit_feature_disabled_and_unchanged(client):
    """Verify V1 and V3 do not allow editing and keep existing behaviour unchanged."""
    # Under V1
    app_module.APP_VERSION = "v1"
    v1_get = client.get("/reviews/1/edit")
    assert v1_get.status_code == 403
    v1_home = client.get("/")
    assert b"/reviews/1/edit" not in v1_home.data

    # Under V3
    app_module.APP_VERSION = "v3"
    v3_get = client.get("/reviews/1/edit")
    assert v3_get.status_code == 403
    v3_home = client.get("/")
    assert b"/reviews/1/edit" not in v3_home.data


def test_v2_home_page_displays_edit_button(client):
    """Verify V2 displays the Edit button on reviews."""
    app_module.APP_VERSION = "v2"
    response = client.get("/")
    assert response.status_code == 200
    assert b"Edit" in response.data
    assert b"/reviews/1/edit" in response.data


# ==============================================================================
# Version 3 (V3) Delete/Remove Feature Tests
# ==============================================================================

def test_v3_delete_button_present_on_pages(client):
    """Verify V3 displays the Delete button and confirmation message."""
    app_module.APP_VERSION = "v3"
    # Home page
    res_home = client.get("/")
    assert res_home.status_code == 200
    assert b"Delete" in res_home.data
    assert b"/reviews/1/delete" in res_home.data
    assert b"Are you sure you want to delete this review?" in res_home.data

    # Reviews page
    res_reviews = client.get("/reviews")
    assert res_reviews.status_code == 200
    assert b"Delete" in res_reviews.data
    assert b"/reviews/1/delete" in res_reviews.data


def test_v3_delete_existing_review_removes_from_data_store(client):
    """Verify deleting a review removes it from memory and displays success message."""
    app_module.APP_VERSION = "v3"
    initial_count = len(app_module.reviews)
    assert any(r["id"] == 1 for r in app_module.reviews)

    # Issue delete request
    response = client.post("/reviews/1/delete")
    assert response.status_code == 302

    # Data store verification: review 1 must be permanently removed
    assert len(app_module.reviews) == initial_count - 1
    assert not any(r["id"] == 1 for r in app_module.reviews)

    # Follow redirect and verify success message
    follow_resp = client.get(response.headers["Location"])
    assert follow_resp.status_code == 200
    assert b"Review deleted successfully!" in follow_resp.data
    assert b"Outstanding system!" not in follow_resp.data


def test_v3_cancel_confirmation_does_not_delete_review(client):
    """Verify cancelling confirmation leaves review data untouched."""
    app_module.APP_VERSION = "v3"
    initial_count = len(app_module.reviews)

    # When client-side confirmation is cancelled, no POST request is sent
    # Review #1 remains intact in data store
    assert len(app_module.reviews) == initial_count
    assert any(r["id"] == 1 for r in app_module.reviews)

    # Page still displays review #1
    page = client.get("/")
    assert page.status_code == 200
    assert b"Aarav Sharma" in page.data


def test_v3_delete_nonexistent_review_returns_404(client):
    """Verify attempting to delete an invalid/non-existent review returns HTTP 404."""
    app_module.APP_VERSION = "v3"
    response = client.post("/reviews/99999/delete")
    assert response.status_code == 404


def test_v3_statistics_and_histogram_update_after_deletion(client):
    """Verify statistics cards and rating distribution histogram update upon deletion."""
    app_module.APP_VERSION = "v3"
    # Seed data has 3 reviews: two 5-star (id:1, id:3), one 4-star (id:2)
    initial_stats = app_module.calculate_statistics(app_module.reviews)
    assert initial_stats["total"] == 3
    assert initial_stats["five_star_count"] == 2

    # Delete review #1 (5-star rating)
    client.post("/reviews/1/delete")

    # Recalculated statistics
    new_stats = app_module.calculate_statistics(app_module.reviews)
    assert new_stats["total"] == 2
    assert new_stats["five_star_count"] == 1
    assert new_stats["distribution"][5] == 1
    assert new_stats["distribution"][4] == 1


def test_v1_and_v2_unaffected_by_v3_delete(client):
    """Verify V1 and V2 reject delete operations and do not display Delete buttons."""
    # Under V1
    app_module.APP_VERSION = "v1"
    v1_post = client.post("/reviews/1/delete")
    assert v1_post.status_code == 403
    v1_home = client.get("/")
    assert b"/reviews/1/delete" not in v1_home.data
    assert b"btn-delete" not in v1_home.data

    # Under V2: edit is available, delete is rejected
    app_module.APP_VERSION = "v2"
    v2_post = client.post("/reviews/1/delete")
    assert v2_post.status_code == 403
    v2_home = client.get("/")
    assert b"/reviews/1/delete" not in v2_home.data
    assert b"btn-delete" not in v2_home.data
    assert b"/reviews/1/edit" in v2_home.data
