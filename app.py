import os
from flask import Flask, request, redirect, url_for, render_template_string

APP_VERSION = os.getenv("APP_VERSION", "v1")
app = Flask(__name__)
reviews = [
    {"name": "Aarav", "rating": 5, "comment": "Easy to use."},
    {"name": "Diya", "rating": 4, "comment": "Works well for my needs."},
]

PAGE = """
<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Review System {{ version }}</title>
<style>
body{font-family:Arial,sans-serif;max-width:850px;margin:35px auto;padding:0 18px;background:#f4f7fb;color:#172033}
header,.card{background:white;border-radius:12px;padding:20px;margin-bottom:18px;box-shadow:0 2px 12px #00000010}
.badge{display:inline-block;padding:6px 10px;border-radius:20px;background:#dbeafe;color:#1d4ed8;font-weight:bold}
input,textarea,select{display:block;width:100%;box-sizing:border-box;padding:10px;margin:8px 0 14px;border:1px solid #cbd5e1;border-radius:7px;font:inherit}
button{padding:10px 16px;border:0;border-radius:7px;background:#2563eb;color:white;font-weight:bold;cursor:pointer}
.review{border-top:1px solid #e2e8f0;padding:12px 0}.muted{color:#64748b}
</style></head><body>
<header><h1>Review System</h1><span class="badge">Application {{ version }}</span>
<p>Submit and view customer reviews in this demonstration application.</p>
<p class="muted">Health status: <a href="/health">/health</a></p></header>
<section class="card"><h2>Add a review</h2>
<form method="post" action="/reviews">
<label for="name">Your name</label><input id="name" name="name" maxlength="60" required>
<label for="rating">Rating</label><select id="rating" name="rating" required>
<option value="5">5 - Excellent</option><option value="4">4 - Very good</option><option value="3">3 - Good</option><option value="2">2 - Fair</option><option value="1">1 - Poor</option>
</select><label for="comment">Comment</label><textarea id="comment" name="comment" maxlength="500" required></textarea>
<button type="submit">Submit review</button></form></section>
<section class="card"><h2>Customer reviews ({{ reviews|length }})</h2>
{% for review in reviews %}<div class="review"><strong>{{ review.name|e }}</strong> — {{ review.rating }}/5<p>{{ review.comment|e }}</p></div>
{% else %}<p>No reviews yet.</p>{% endfor %}</section></body></html>
"""

@app.get("/")
def home():
    return render_template_string(PAGE, version=APP_VERSION, reviews=reviews)

@app.post("/reviews")
def add_review():
    name = request.form.get("name", "").strip()
    comment = request.form.get("comment", "").strip()
    try:
        rating = int(request.form.get("rating", "0"))
    except ValueError:
        rating = 0
    if not name or not comment or rating not in range(1, 6):
        return "Invalid review. Provide a name, comment, and rating from 1 to 5.", 400
    reviews.insert(0, {"name": name[:60], "rating": rating, "comment": comment[:500]})
    return redirect(url_for("home"))

@app.get("/health")
def health():
    return {"status": "healthy", "version": APP_VERSION}, 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", "5000")))
