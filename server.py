import os
import json
import datetime
from flask import Flask, request, jsonify
from Recommender_Logic import ListingRecommender
from rental_management import create_user_profile, view_user_profile, edit_user_profile, create_booking, delete_booking, delete_profile
from Filter_And_Sort import filter_properties, sort_properties_asjson


app = Flask(__name__)

ALLOWED_ENVS = ["beach","lake","forest","mountains","nightlife","remote","glamping","city","modern","historic"]

def _normalize_date(s):
    # accepts YYYY-MM-DD or YYYY/M/D; returns strict YYYY-MM-DD or None
    try:
        return datetime.datetime.strptime(s.strip(), '%Y-%m-%d').strftime('%Y-%m-%d')
    except Exception:
        try:
            dt = datetime.datetime.strptime(s.strip(), '%Y/%m/%d')
            return dt.strftime('%Y-%m-%d')
        except Exception:
            return None

def _date_list_inclusive(start_iso, end_iso):
    start_dt = datetime.datetime.strptime(start_iso, '%Y-%m-%d').date()
    end_dt = datetime.datetime.strptime(end_iso, '%Y-%m-%d').date()
    out = []
    cur = start_dt
    while cur <= end_dt:
        out.append(cur.strftime('%Y-%m-%d'))
        cur += datetime.timedelta(days=1)
    return out

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


@app.route("/profile", methods=["POST", "OPTIONS"])
def profile():
    if request.method == "OPTIONS":
        return ("", 204)
    data = request.get_json(silent=True) or {}
    user_id = (data.get("userId") or "").strip()
    if not user_id:
        return jsonify(error="userId is required"), 400

    try:
        u = view_user_profile(user_id)  # returns a dict or None
        if not u:
            return jsonify(error="user not found"), 404

        # map backend -> frontend shape
        out = {
            "id": u.get("user_id"),
            "name": u.get("name"),
            "password": u.get("password") or "",
            "groupSize": u.get("group_size"),
            "preferredEnv": u.get("preferred_environment"),
            "budgetRange": u.get("budget_range") or [],
            "bookingHistory": [
                {"propertyId": b.get("property_id"), "start": b.get("start_date"), "end": b.get("end_date")}
                for b in (u.get("booking_history") or [])
            ],
        }
        return jsonify(profile=out)
    except Exception as e:
        import traceback; traceback.print_exc()
        return jsonify(error=str(e)), 500
    


@app.route("/profile/update", methods=["POST", "OPTIONS"])
def profile_update():
    if request.method == "OPTIONS":
        return ("", 204)
    data = request.get_json(silent=True) or {}
    user_id = (data.get("userId") or "").strip()
    if not user_id:
        return jsonify(error="userId is required"), 400

    # map frontend -> rental_management keys
    new_user = {"user_id": user_id}
    if "name" in data: new_user["name"] = data["name"]
    if "password" in data: new_user["password"] = data["password"]
    if "groupSize" in data: new_user["group_size"] = data["groupSize"]
    if "preferredEnv" in data: new_user["preferred_environment"] = data["preferredEnv"]
    if "budgetRange" in data:
        br = data["budgetRange"]
        if isinstance(br, list) and len(br) == 2:
            new_user["budget_range"] = br

    try:
        edit_user_profile(new_user, users_file_path=os.path.join(os.path.dirname(__file__), "data", "Users.json"))
        u = view_user_profile(user_id, file_path=os.path.join(os.path.dirname(__file__), "data", "Users.json"))
        if not u:
            return jsonify(error="user not found after update"), 404
        out = {
            "id": u.get("user_id"),
            "name": u.get("name"),
            "password": u.get("password") or "",
            "groupSize": u.get("group_size"),
            "preferredEnv": u.get("preferred_environment"),
            "budgetRange": u.get("budget_range") or [],
            "bookingHistory": [
                {"propertyId": b.get("property_id"), "start": b.get("start_date"), "end": b.get("end_date")}
                for b in (u.get("booking_history") or [])
            ],
        }
        return jsonify(profile=out)
    except Exception as e:
        import traceback; traceback.print_exc()
        return jsonify(error=str(e)), 500
    
@app.route("/booking/delete", methods=["POST", "OPTIONS"])
def booking_delete():
    if request.method == "OPTIONS":
        return ("", 204)
    data = request.get_json(silent=True) or {}
    user_id = (data.get("userId") or "").strip()
    property_id = (data.get("propertyId") or "").strip()
    start = data.get("start")
    end = data.get("end")
    if not (user_id and property_id and start and end):
        return jsonify(error="Missing required fields"), 400
    try:
        ok = delete_booking(
            user_id, property_id, start, end,
            users_file_path=os.path.join(os.path.dirname(__file__), "data", "Users.json"),
            properties_file_path=os.path.join(os.path.dirname(__file__), "data", "Properties.json"),
        )
        if not ok:
            return jsonify(error="Delete failed"), 400
        u = view_user_profile(user_id, file_path=os.path.join(os.path.dirname(__file__), "data", "Users.json"))
        if not u:
            return jsonify(error="User not found"), 404
        bh = [
            {"propertyId": b.get("property_id"), "start": b.get("start_date"), "end": b.get("end_date")}
            for b in (u.get("booking_history") or [])
        ]
        return jsonify(ok=True, bookingHistory=bh)
    except Exception as e:
        import traceback; traceback.print_exc()
        return jsonify(error=str(e)), 500
    
@app.route("/account/delete", methods=["POST", "OPTIONS"])
def account_delete():
    if request.method == "OPTIONS":
        return ("", 204)
    data = request.get_json(silent=True) or {}
    user_id = (data.get("userId") or "").strip()
    if not user_id:
        return jsonify(error="userId is required"), 400
    try:
        # delete_profile uses default file path; keep consistent with your repo
        delete_profile(user_id)
        return jsonify(ok=True)
    except Exception as e:
        import traceback; traceback.print_exc()
        return jsonify(error=str(e)), 500
    
    
@app.route("/booking/create", methods=["POST", "OPTIONS"])
def booking_create():
    if request.method == "OPTIONS":
        return ("", 204)
    data = request.get_json(silent=True) or {}
    user_id = (data.get("userId") or "").strip()
    property_id = (data.get("propertyId") or "").strip()
    start_raw = (data.get("start") or "").strip()
    end_raw = (data.get("end") or "").strip()
    start = _normalize_date(start_raw)
    end = _normalize_date(end_raw)
    if not (user_id and property_id and start and end):
        return jsonify(error="Missing or invalid fields"), 400

    # order check
    sdt = datetime.datetime.strptime(start, '%Y-%m-%d').date()
    edt = datetime.datetime.strptime(end, '%Y-%m-%d').date()
    if edt < sdt:
        return jsonify(error="End date cannot be before the start date."), 400

    # availability check
    try:
        with open(os.path.join(os.path.dirname(__file__), "data", "Properties.json"), "r", encoding="utf-8") as f:
            props = json.load(f)
        prop = next((p for p in props if p.get("property_id") == property_id), None)
        if not prop:
            return jsonify(error="Property not found"), 404
        req_dates = set(_date_list_inclusive(start, end))
        existing = set(prop.get("unavailable_dates", []))
        if existing.intersection(req_dates):
            return jsonify(error="This property is not available for the selected dates."), 409
    except Exception as e:
        return jsonify(error=str(e)), 500

    # persist via domain function
    ok = create_booking(user_id, property_id, start, end)
    if not ok:
        return jsonify(error="Failed to create booking."), 400
    return jsonify(ok=True)


@app.route("/register", methods=["POST","OPTIONS"])
def register():
    if request.method == "OPTIONS":
        return ("", 204)
    data = request.get_json(silent=True) or {}
    username = (data.get("userId") or "").strip()
    name = (data.get("name") or "").strip()
    password = data.get("password")
    preferred = (data.get("preferredEnv") or "").strip()
    budget = data.get("budgetRange") or []
    group_size = data.get("groupSize")

    # basic validations
    if not (username and name and password):
        return jsonify(error="Missing required fields"), 400
    try:
        group_size = int(group_size)
    except Exception:
        return jsonify(error="Group size must be an integer"), 400
    if not (1 <= group_size <= 10):
        return jsonify(error="Group size must be between 1 and 10"), 400
    if preferred not in ALLOWED_ENVS:
        return jsonify(error="Invalid preferred environment"), 400
    if not (isinstance(budget, list) and len(budget) == 2):
        return jsonify(error="Budget range must be [min,max]"), 400
    try:
        bmin, bmax = int(budget[0]), int(budget[1])
    except Exception:
        return jsonify(error="Budget values must be integers"), 400
    if bmin <= 0 or bmax < bmin:
        return jsonify(error="Budget range invalid (min > 0 and max >= min)"), 400

    # uniqueness
    users_path = os.path.join(os.path.dirname(__file__), "data", "Users.json")
    try:
        with open(users_path, "r", encoding="utf-8") as f:
            users = json.load(f)
    except Exception:
        users = []
    if any(u.get("user_id") == username for u in users):
        return jsonify(error="This username has been used. Please choose another one."), 409

    # create
    ok = create_user_profile(username, name, password, group_size, preferred, [bmin, bmax], file_path=users_path)
    if not ok:
        return jsonify(error="Failed to create user"), 500

    return jsonify(ok=True, userId=username, name=name)


@app.route("/search", methods=["POST","OPTIONS"])
def search():
    if request.method == "OPTIONS":
        return ("", 204)
    data = request.get_json(silent=True) or {}

    # Read optional filters
    location     = (data.get("location") or "").strip() or None
    prop_type    = (data.get("propType") or "").strip() or None
    features     = data.get("features") or None
    tags         = data.get("tags") or None
    start_date   = (data.get("startDate") or "").strip() or None
    end_date     = (data.get("endDate") or "").strip() or None

    # Validate numeric fields
    group_size = data.get("groupSize")
    if group_size is not None:
        try:
            group_size = int(group_size)
        except Exception:
            return jsonify(error="Group size must be an integer"), 400
        if not (1 <= group_size <= 10):
            return jsonify(error="Group size must be between 1 and 10"), 400

    min_price = data.get("minPrice")
    max_price = data.get("maxPrice")
    if min_price is not None:
        try:
            min_price = int(min_price)
        except Exception:
            return jsonify(error="Min price must be an integer"), 400
        if min_price < 0:
            return jsonify(error="Min price must be >= 0"), 400
    if max_price is not None:
        try:
            max_price = int(max_price)
        except Exception:
            return jsonify(error="Max price must be an integer"), 400
        if max_price < 0:
            return jsonify(error="Max price must be >= 0"), 400
    if min_price is not None and max_price is not None and max_price < min_price:
        return jsonify(error="Max price must be >= min price"), 400

    # Date order (Filter_And_Sort also validates, but we give earlier feedback)
    if start_date and end_date:
        try:
            sdt = datetime.datetime.strptime(start_date, "%Y-%m-%d").date()
            edt = datetime.datetime.strptime(end_date, "%Y-%m-%d").date()
        except Exception:
            return jsonify(error="Dates must be YYYY-MM-DD"), 400
        if edt < sdt:
            return jsonify(error="End date must be on or after start date"), 400

    try:
        results = filter_properties(
            group_size=group_size,
            min_price=min_price,
            max_price=max_price,
            features=features,
            tags=tags,
            prop_type=prop_type,
            location=location,
            start_date=start_date,
            end_date=end_date
        )
        # Map to frontend shape (same as /recommend)
        out = [{
            "id": p.get("property_id"),
            "location": p.get("location"),
            "type": p.get("type"),
            "pricePerNight": p.get("price_per_night"),
            "features": p.get("features") or [],
            "tags": p.get("tags") or [],
            "guestCapacity": p.get("guest_capacity"),
        } for p in (results or [])]
        return jsonify(properties=out)
    except Exception as e:
        import traceback; traceback.print_exc()
        return jsonify(error=str(e)), 500

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5050, debug=True)