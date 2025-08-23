from flask import Flask, request, jsonify
import os, json
from Recommender_Logic import ListingRecommender

app = Flask(__name__)

@app.after_request
def add_cors(resp):
    resp.headers["Access-Control-Allow-Origin"] = "*"
    resp.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization"
    resp.headers["Access-Control-Allow-Methods"] = "GET, POST, OPTIONS"
    return resp


@app.route("/recommend", methods=["POST", "OPTIONS"])
def recommend():
    if request.method == "OPTIONS":
        return ("", 204)
    data = request.get_json(silent=True) or {}
    user_id = (data.get("userId") or data.get("userid") or "").strip()
    if not user_id:
        return jsonify(error="userId is required"), 400

    # Run recommender
    try:
        rec = ListingRecommender()
        rows = rec.calculate_total_score(user_id)  # list of dicts

        # Map to frontend shape (id/pricePerNight/guestCapacity/etc.)
        out = [{
            "id": r.get("property_id"),
            "location": r.get("location"),
            "type": r.get("type"),
            "pricePerNight": r.get("price_per_night"),
            "features": r.get("features") or [],
            "tags": r.get("tags") or [],
            "guestCapacity": r.get("guest_capacity"),
        } for r in rows if isinstance(r, dict)]

        return jsonify(properties=out)
    except Exception as e:
        import traceback; traceback.print_exc()
        return jsonify(error=str(e)), 500


@app.route("/assistant", methods=["POST", "OPTIONS"])
def assistant():
    if request.method == "OPTIONS":
        return ("", 204)
    data = request.get_json(silent=True) or {}
    user_input = (data.get("user_input") or data.get("prompt") or "").strip()
    history = data.get("messages")
    try:
        from LLM_functions import generate_suggestions_text
        text = generate_suggestions_text(user_input=user_input, messages=history)
        return jsonify(text=text)
    except Exception as e:
        import traceback; traceback.print_exc()   # prints full stack
        return jsonify(error=str(e)), 500
    
    
@app.route("/login", methods=["POST", "OPTIONS"])
def login():
    if request.method == "OPTIONS":
        return ("", 204)
    data = request.get_json(silent=True) or {}
    user_id = (data.get("userId") or "").strip()
    password = data.get("password")
    if not user_id or password is None:
        return jsonify(error="Missing credentials"), 400
    try:
        with open(os.path.join(os.path.dirname(__file__), "data", "Users.json"), "r", encoding="utf-8") as f:
            users = json.load(f)
        user = next((u for u in users if u.get("user_id") == user_id and u.get("password") == password), None)
        if not user:
            return jsonify(error="Invalid username or password"), 401
        return jsonify(ok=True, user_id=user_id, name=user.get("name"))
    except Exception as e:
        import traceback; traceback.print_exc()
        return jsonify(error=str(e)), 500

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5050, debug=True)