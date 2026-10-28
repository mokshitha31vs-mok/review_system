"""
Review System Web Application
A lightweight Flask application for collecting, validating, displaying,
and analyzing user reviews. Built for CI/CD demonstration with Docker,
Jenkins, and Kubernetes across progressive application versions (V1, V2, V3).

Persistence Note:
Reviews are kept in-memory for fast execution, zero external database setup,
and idempotent automated testing. State is reset when container restarts.
"""

from datetime import datetime
import os
from flask import Flask, flash, jsonify, redirect, render_template, request, url_for

# Application version configured via environment variable (default: v1)
APP_VERSION = os.getenv("APP_VERSION", "v1").lower().strip()

app = Flask(__name__)
# Secret key required for session flash messages
app.secret_key = os.getenv("SECRET_KEY", "ci-cd-review-system-secret-key-2026")

# In-memory storage for reviews
reviews = [
    {
        "id": 1,
        "name": "Aarav Sharma",
        "rating": 5,
        "comment": "Outstanding system! The UI is very intuitive and responsive.",
        "created_at": "2026-10-28 10:15",
        "timestamp": 1729988100,
    },
    {
        "id": 2,
        "name": "Diya Patel",
        "rating": 4,
        "comment": "Great workflow and clear feedback display. Works seamlessly.",
        "created_at": "2026-10-28 11:30",
        "timestamp": 1729992600,
    },
    {
        "id": 3,
        "name": "Rohan Kumar",
        "rating": 5,
        "comment": "Fast loading times and clean interface. Exactly what we needed.",
        "created_at": "2026-10-28 12:45",
        "timestamp": 1729997100,
    },
]


def calculate_statistics(reviews_list):
    """Calculate aggregate statistics for V2 and V3 analytics."""
    total = len(reviews_list)
    if total == 0:
        return {
            "total": 0,
            "avg_rating": 0.0,
            "five_star_count": 0,
            "positive_pct": 0.0,
            "distribution": {5: 0, 4: 0, 3: 0, 2: 0, 1: 0},
            "distribution_pct": {5: 0.0, 4: 0.0, 3: 0.0, 2: 0.0, 1: 0.0},
        }

    sum_ratings = sum(r["rating"] for r in reviews_list)
    avg_rating = round(sum_ratings / total, 1)

    distribution = {5: 0, 4: 0, 3: 0, 2: 0, 1: 0}
    for r in reviews_list:
        star = r.get("rating", 0)
        if star in distribution:
            distribution[star] += 1

    distribution_pct = {
        star: round((count / total) * 100, 1)
        for star, count in distribution.items()
    }

    five_star_count = distribution[5]
    # Positive ratings: 4 and 5 stars
    positive_count = distribution[5] + distribution[4]
    positive_pct = round((positive_count / total) * 100, 1)

    return {
        "total": total,
        "avg_rating": avg_rating,
        "five_star_count": five_star_count,
        "positive_pct": positive_pct,
        "distribution": distribution,
        "distribution_pct": distribution_pct,
    }


@app.route("/", methods=["GET"])
def home():
    """Home page: renders review submission form, statistics, and reviews list."""
    current_filter = request.args.get("filter_rating", "all").strip().lower()
    current_sort = request.args.get("sort_by", "newest").strip().lower()

    filtered_list = list(reviews)

    # Filter feature available in V2 and V3
    if APP_VERSION in ["v2", "v3"] and current_filter in ["1", "2", "3", "4", "5"]:
        target_star = int(current_filter)
        filtered_list = [r for r in filtered_list if r["rating"] == target_star]

    # Sorting feature available in V3
    if APP_VERSION == "v3":
        if current_sort == "oldest":
            filtered_list = sorted(filtered_list, key=lambda x: x.get("timestamp", 0))
        elif current_sort == "highest":
            filtered_list = sorted(filtered_list, key=lambda x: x["rating"], reverse=True)
        elif current_sort == "lowest":
            filtered_list = sorted(filtered_list, key=lambda x: x["rating"])
        else:  # newest first
            filtered_list = sorted(filtered_list, key=lambda x: x.get("timestamp", 0), reverse=True)

    stats = calculate_statistics(reviews)

    return render_template(
        "index.html",
        version=APP_VERSION,
        reviews=reviews,
        filtered_reviews=filtered_list,
        stats=stats,
        current_filter=current_filter,
        current_sort=current_sort,
    )


@app.route("/reviews", methods=["GET"])
def reviews_page():
    """All reviews registry page."""
    stats = calculate_statistics(reviews)
    return render_template(
        "reviews.html",
        version=APP_VERSION,
        reviews=reviews,
        stats=stats,
    )


@app.route("/reviews", methods=["POST"])
def submit_review():
    """Handle review submission with comprehensive validation."""
    name = request.form.get("name", "").strip()
    comment = request.form.get("comment", "").strip()
    rating_raw = request.form.get("rating", "").strip()

    try:
        rating = int(rating_raw)
    except (ValueError, TypeError):
        rating = 0

    # Validation: empty values or invalid rating range
    if not name or len(name) > 60:
        return (
            "Invalid review submission: Name is required and must not exceed 60 characters.",
            400,
        )

    if not comment or len(comment) > 500:
        return (
            "Invalid review submission: Comment is required and must not exceed 500 characters.",
            400,
        )

    if rating not in range(1, 6):
        return (
            "Invalid review submission: Rating must be an integer between 1 and 5.",
            400,
        )

    now = datetime.now()
    new_review = {
        "id": len(reviews) + 1,
        "name": name,
        "rating": rating,
        "comment": comment,
        "created_at": now.strftime("%Y-%m-%d %H:%M"),
        "timestamp": int(now.timestamp()),
    }

    reviews.insert(0, new_review)
    flash("Thank you! Your review has been submitted successfully.", "success")
    return redirect(url_for("home"))


@app.route("/health", methods=["GET"])
def health():
    """Health check endpoint for Docker container checks and Kubernetes probes."""
    return jsonify({
        "status": "healthy",
        "version": APP_VERSION,
    }), 200


if __name__ == "__main__":
    port = int(os.getenv("PORT", "5000"))
    app.run(host="0.0.0.0", port=port, debug=False)
