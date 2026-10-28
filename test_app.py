import app as app_module

def client():
    app_module.app.config["TESTING"] = True
    return app_module.app.test_client()

def test_home_page_returns_200():
    response = client().get("/")
    assert response.status_code == 200
    assert b"Review System" in response.data

def test_health_endpoint_is_healthy():
    response = client().get("/health")
    assert response.status_code == 200
    assert response.json["status"] == "healthy"

def test_health_endpoint_includes_version():
    response = client().get("/health")
    assert "version" in response.json

def test_submit_review_redirects_to_home():
    response = client().post("/reviews", data={"name": "Test User", "rating": "5", "comment": "Great app!"})
    assert response.status_code == 302
    assert response.headers["Location"].endswith("/")

def test_invalid_review_is_rejected():
    response = client().post("/reviews", data={"name": "", "rating": "9", "comment": ""})
    assert response.status_code == 400
