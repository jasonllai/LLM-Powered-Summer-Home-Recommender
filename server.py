from flask import Flask, request, jsonify

app = Flask(__name__)

@app.after_request
def add_cors(resp):
    resp.headers["Access-Control-Allow-Origin"] = "*"
    resp.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization"
    resp.headers["Access-Control-Allow-Methods"] = "GET, POST, OPTIONS"
    return resp

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

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5050, debug=True)