import os
import json
import datetime
from flask import Flask, request, jsonify
from Recommender_Logic import ListingRecommender
from filter import filter_properties, sort_properties_asjson
from LLM_functions import location_pool, type_pool, feature_pool, tag_pool, generate_properties
from rental_management import create_user_profile, view_user_profile, edit_user_profile, create_booking, delete_booking, delete_profile, validate_admin, validate_user, update_property, delete_property, view_properties, add_properties


app = Flask(__name__)

# Fixed whitelist for registration's preferred environment input (used to validate /register)
ALLOWED_ENVS = ["beach","lake","forest","mountains","nightlife","remote","glamping","city","modern","historic"]


# ---- Helpers ----
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


# ---- Flask routes ----
@app.after_request
def add_cors(resp):
    # Simple CORS allow-all for local development (consider scoping origins for production)
    resp.headers["Access-Control-Allow-Origin"] = "*"
    resp.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization"
    resp.headers["Access-Control-Allow-Methods"] = "GET, POST, OPTIONS"
    return resp


# ---- User routes ----
@app.route("/recommend", methods=["POST", "OPTIONS"])
def recommend():
    # Returns top recommended properties for a user (normalized to frontend shape)
    if request.method == "OPTIONS":
        return ("", 204)
    data = request.get_json(silent=True) or {}
    user_id = (data.get("userId") or data.get("userid") or "").strip()
    if not user_id:
        return jsonify(error="userId is required"), 400

    try:
        rec = ListingRecommender()
        rows = rec.calculate_total_score(user_id)  # domain logic

        # Map domain fields → UI fields
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
    # Proxy to LLM: calls TripBuddy prompt builder and returns Markdown text
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
        import traceback; traceback.print_exc()
        return jsonify(error=str(e)), 500
    
    
@app.route("/login", methods=["POST", "OPTIONS"])
def login():
    # Basic login against Users.json (plaintext; replace with hashed auth for production)
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
    # Load and map a user's profile to the frontend shape
    if request.method == "OPTIONS":
        return ("", 204)
    data = request.get_json(silent=True) or {}
    user_id = (data.get("userId") or "").strip()
    if not user_id:
        return jsonify(error="userId is required"), 400

    try:
        u = view_user_profile(user_id)  # domain read; returns raw domain dict
        if not u:
            return jsonify(error="user not found"), 404

        # Map domain → UI fields
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
    # Partial profile update; translates UI keys → domain keys, persists, returns updated view
    if request.method == "OPTIONS":
        return ("", 204)
    data = request.get_json(silent=True) or {}
    user_id = (data.get("userId") or "").strip()
    if not user_id:
        return jsonify(error="userId is required"), 400

    # Map UI fields → domain fields (only provided keys are updated)
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
    # Removes a booking and returns updated bookingHistory in UI shape
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
    # Deletes a user profile; id taken from JSON body
    if request.method == "OPTIONS":
        return ("", 204)
    data = request.get_json(silent=True) or {}
    user_id = (data.get("userId") or "").strip()
    if not user_id:
        return jsonify(error="userId is required"), 400
    try:
        delete_profile(user_id)
        return jsonify(ok=True)
    except Exception as e:
        import traceback; traceback.print_exc()
        return jsonify(error=str(e)), 500
    
    
@app.route("/booking/create", methods=["POST", "OPTIONS"])
def booking_create():
    # Creates a booking after date normalization, order check, and availability check
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

    # Ensure end >= start
    sdt = datetime.datetime.strptime(start, '%Y-%m-%d').date()
    edt = datetime.datetime.strptime(end, '%Y-%m-%d').date()
    if edt < sdt:
        return jsonify(error="End date cannot be before the start date."), 400

    # Ensure requested dates are not already unavailable for the property
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

    ok = create_booking(user_id, property_id, start, end)
    if not ok:
        return jsonify(error="Failed to create booking."), 400
    return jsonify(ok=True)


@app.route("/register", methods=["POST","OPTIONS"])
def register():
    # Creates a user with basic validations; ensures uniqueness by user_id
    if request.method == "OPTIONS":
        return ("", 204)
    data = request.get_json(silent=True) or {}
    username = (data.get("userId") or "").strip()
    name = (data.get("name") or "").strip()
    password = data.get("password")
    preferred = (data.get("preferredEnv") or "").strip()
    budget = data.get("budgetRange") or []
    group_size = data.get("groupSize")

    # Validations: required fields, integer ranges, allowed enums, budget pair
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

    # Uniqueness check (Users.json)
    users_path = os.path.join(os.path.dirname(__file__), "data", "Users.json")
    try:
        with open(users_path, "r", encoding="utf-8") as f:
            users = json.load(f)
    except Exception:
        users = []
    if any(u.get("user_id") == username for u in users):
        return jsonify(error="This username has been used. Please choose another one."), 409

    ok = create_user_profile(username, name, password, group_size, preferred, [bmin, bmax], file_path=users_path)
    if not ok:
        return jsonify(error="Failed to create user"), 500

    return jsonify(ok=True, userId=username, name=name)


@app.route("/search", methods=["POST","OPTIONS"])
def search():
    # Searches properties with optional filters; validates numbers and date order
    if request.method == "OPTIONS":
        return ("", 204)
    data = request.get_json(silent=True) or {}

    # Optional filters (normalize empty strings to None)
    location     = (data.get("location") or "").strip() or None
    prop_type    = (data.get("propType") or "").strip() or None
    features     = data.get("features") or None
    tags         = data.get("tags") or None
    start_date   = (data.get("startDate") or "").strip() or None
    end_date     = (data.get("endDate") or "").strip() or None

    # Numbers: group size and prices
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

    # Dates: order and format
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
        # Normalize to UI fields
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

    
    
# ---- Admin routes ----
@app.route("/admin/login", methods=["POST", "OPTIONS"])
def admin_login():
    # Admin login using domain validator (separate from user login)
    if request.method == "OPTIONS":
        return ("", 204)
    data = request.get_json(silent=True) or {}
    admin_id = (data.get("userId") or "").strip()
    password = data.get("password")
    if not admin_id or password is None:
        return jsonify(error="Missing credentials"), 400
    try:
        ok = validate_admin(admin_id, password)
        if not ok:
            return jsonify(error="Invalid admin credentials"), 401
        return jsonify(ok=True, admin_id=admin_id)
    except Exception as e:
        import traceback; traceback.print_exc()
        return jsonify(error=str(e)), 500
    
    
@app.route("/admin/users", methods=["GET", "POST", "OPTIONS"])
def admin_users():
    # Lists users and expands recent bookings; includes a "pretty" property name
    if request.method == "OPTIONS":
        return ("", 204)
    try:
        users = view_user_profile.__globals__["load_data_from_json"](os.path.join(os.path.dirname(__file__), "data", "Users.json")) or []
        with open(os.path.join(os.path.dirname(__file__), "data", "Properties.json"), "r", encoding="utf-8") as f:
            props = json.load(f)
        name_by_id = {p.get("property_id"): f"{p.get('type')} in {p.get('location')}" for p in props}

        out = []
        for u in users:
            out.append({
                "id": u.get("user_id"),
                "name": u.get("name"),
                "groupSize": u.get("group_size"),
                "preferredEnv": u.get("preferred_environment"),
                "budgetRange": u.get("budget_range") or [],
                "bookingHistory": [
                    {
                        "propertyId": b.get("property_id"),
                        "propertyName": name_by_id.get(b.get("property_id"), "(unknown)"),
                        "start": b.get("start_date"),
                        "end": b.get("end_date"),
                    }
                    for b in (u.get("booking_history") or [])
                ]
            })
        return jsonify(users=out)
    except Exception as e:
        import traceback; traceback.print_exc()
        return jsonify(error=str(e)), 500
    
    
@app.route("/admin/properties", methods=["POST","OPTIONS"])
def admin_properties():
    # Returns all properties for admin management
    if request.method == "OPTIONS":
        return ("", 204)
    try:
        props = view_properties(file_path=os.path.join(os.path.dirname(__file__), "data", "Properties.json")) or []
        return jsonify(properties=props)
    except Exception as e:
        import traceback; traceback.print_exc()
        return jsonify(error=str(e)), 500
    

@app.route("/admin/property/update", methods=["POST","OPTIONS"])
def admin_property_update():
    # Updates a property; validates enums, numbers, and keeps unavailable_dates unless provided
    if request.method == "OPTIONS":
        return ("", 204)
    data = request.get_json(silent=True) or {}
    p = data if isinstance(data, dict) else {}
    required = ["property_id","location","type","price_per_night","features","tags","guest_capacity"]
    if not all(k in p for k in required):
        return jsonify(error="Missing fields"), 400

    # Enum and numeric validations (rely on pools imported from LLM_functions)
    if p["location"] not in location_pool: return jsonify(error="Invalid location"), 400
    if p["type"] not in type_pool: return jsonify(error="Invalid type"), 400
    try:
        price = int(p["price_per_night"])
        if price <= 0: raise ValueError()
    except Exception:
        return jsonify(error="price_per_night must be a positive integer"), 400
    try:
        cap = int(p["guest_capacity"])
        if not (1 <= cap <= 10): raise ValueError()
    except Exception:
        return jsonify(error="guest_capacity must be 1–10"), 400
    if not set(p.get("features") or []).issubset(set(feature_pool)):
        return jsonify(error="features contain invalid values"), 400
    if not set(p.get("tags") or []).issubset(set(tag_pool)):
        return jsonify(error="tags contain invalid values"), 400

    # Preserve current unavailable_dates unless explicitly sent by client
    if "unavailable_dates" not in p:
        try:
            with open(os.path.join(os.path.dirname(__file__), "data", "Properties.json"), "r", encoding="utf-8") as f:
                props = json.load(f)
            cur = next((x for x in props if x.get("property_id")==p["property_id"]), {})
            p["unavailable_dates"] = cur.get("unavailable_dates", [])
        except Exception:
            p["unavailable_dates"] = []

    try:
        update_property(p, file_path=os.path.join(os.path.dirname(__file__), "data", "Properties.json"))
        return jsonify(ok=True)
    except Exception as e:
        import traceback; traceback.print_exc()
        return jsonify(error=str(e)), 500
    

@app.route("/admin/property/delete", methods=["POST","OPTIONS"])
def admin_property_delete():
    # Deletes a property (and cleans up related data in users, if needed by domain)
    if request.method == "OPTIONS":
        return ("", 204)
    data = request.get_json(silent=True) or {}
    pid = (data.get("propertyId") or "").strip()
    if not pid: return jsonify(error="propertyId required"), 400
    try:
        delete_property(pid,
                        file_path=os.path.join(os.path.dirname(__file__), "data", "Properties.json"),
                        users_file_path=os.path.join(os.path.dirname(__file__), "data", "Users.json"))
        return jsonify(ok=True)
    except Exception as e:
        import traceback; traceback.print_exc()
        return jsonify(error=str(e)), 500
    
    
@app.route("/admin/property/create", methods=["POST","OPTIONS"])
def admin_property_create():
    # Creates a new property; validates enums, numbers, and requires at least one feature/tag
    if request.method == "OPTIONS":
        return ("", 204)
    data = request.get_json(silent=True) or {}
    location = (data.get("location") or "").strip()
    ptype    = (data.get("type") or "").strip()
    features = data.get("features") or []
    tags     = data.get("tags") or []
    try:
        price = int(data.get("price_per_night"))
        cap   = int(data.get("guest_capacity"))
    except Exception:
        return jsonify(error="price_per_night and guest_capacity must be integers"), 400

    if not location: return jsonify(error="Location is required"), 400
    if not ptype:    return jsonify(error="Type is required"), 400
    if price <= 1:   return jsonify(error="Price per night must be > 1"), 400
    if not (1 <= cap <= 10): return jsonify(error="Guest capacity must be 1–10"), 400
    if location not in location_pool: return jsonify(error="Invalid location"), 400
    if ptype not in type_pool:        return jsonify(error="Invalid type"), 400
    if not features or not set(features).issubset(set(feature_pool)):
        return jsonify(error="Invalid or missing features"), 400
    if not tags or not set(tags).issubset(set(tag_pool)):
        return jsonify(error="Invalid or missing tags"), 400

    try:
        add_properties(location, ptype, price, features, tags, cap)
        return jsonify(ok=True)
    except Exception as e:
        import traceback; traceback.print_exc()
        return jsonify(error=str(e)), 500
    
    
@app.route("/admin/properties/generate", methods=["POST","OPTIONS"])
def admin_properties_generate():
    # Triggers LLM-backed property generation; validates n ≥ 1
    if request.method == "OPTIONS":
        return ("", 204)
    data = request.get_json(silent=True) or {}
    try:
        n = int(data.get("n"))
    except Exception:
        return jsonify(error="n must be a positive integer"), 400
    if n < 1:
        return jsonify(error="n must be >= 1"), 400

    try:
        generate_properties(n)
        return jsonify(ok=True, generated=n)
    except Exception as e:
        import traceback; traceback.print_exc()
        return jsonify(error=str(e)), 500


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5050, debug=True)