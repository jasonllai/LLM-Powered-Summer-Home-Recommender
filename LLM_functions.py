import os
import re
import uuid
import json
import time
import requests
from textwrap import dedent
from string import Template


type_pool = ["cabin", "apartment", "cottage", "loft", "villa", "tiny house", "studio"]

location_pool = ["Vancouver", "Toronto", "Montreal", "Calgary", "Edmonton", 
                 "Winnipeg", "Halifax", "Victoria", "Quebec City", "Fredericton"]

feature_pool = ["mountain view", "city skyline view", "lakefront", "riverfront",
                "oceanfront", "beach access", "balcony or patio", "rooftop terrace",
                "private hot tub", "sauna", "private pool", "fireplace", "houskeeper service",
                "BBQ grill", "full kitchen", "chef's kitchen", "EV charger", "free parking",
                "garage", "air conditioning", "heating", "washer and dryer", "fast wifi",
                "dedicated workspace", "smart TV with streaming", "game room", "fitness room",
                "ski-in/ski-out", "wheelchair accessible", "pet-friendly"]

tag_pool = ["mountains", "remote", "adventure", "beach", "city", "lake", 
            "river", "ocean", "forest", "park", "national park", "state park", 
            "national forest", "state forest", "modern","rustic","historic",
            "family-friendly","kid-friendly","pet-friendly","romantic","business-travel",
            "nightlife","eco-friendly","spa","golf","foodie","farm-stay","glamping","long-term"]



DATA_PROMPT = Template(dedent("""
You are a data generator.

TASK
- Produce a JSON array of ${n} objects that summarize properties listed on a summer home rental website.

STRICT SCHEMA
{
    "property_id": "string, UUID v4",
    "location": "string, pick one from ${location_pool}",
    "type": "string, pick one from ${type_pool}",
    "price_per_night": "number, pick one from 50-2000",
    "features": ["list of strings, pick three or more from ${feature_pool}"],
    "tags": ["list of strings, pick three or more from ${tag_pool}"],
    "guest_capacity": "number, pick one from 1-10",
    "unavailable_dates": ["empty list"]
}

CONSISTENCY RULES
- Features and tags MUST be coherent; avoid mutually exclusive geography or vibe.
- Never combine these pairs in the same object:
  - "remote" with "city" or "nightlife" or "business-travel"
  - "beach" or "ocean" or "oceanfront" with "mountains" or "ski-in/ski-out" or "lake" or "river"
  - "lake" with "oceanfront" or "beach" or "riverfront"
  - "river" with "oceanfront" or "beach"
  - "historic" with "modern"
- If a waterfront feature is chosen, align tags accordingly:
  - "oceanfront"/"beach access" -> ocean/beach tags only (no lake/river/mountain)
  - "lakefront" -> lake tags only (no ocean/beach/river/mountain)
  - "riverfront" -> river tags only (no ocean/beach/lake/mountain)

OUTPUT RULES
- Output ONLY valid JSON. No explanations.
- Top-level value MUST be a JSON array.
- No trailing commas.
BEGIN JSON
""").strip())



CHAT_PROMPT = Template(dedent("""
You are TripBuddy, a helpful travel AI.

GOAL
- Given a user's preferences as this: ${user_input}, write a snappy destination blurb and suggest tailored activities.

STYLE
- Friendly, concise, practical. Use short paragraphs and bullets. No fluff.
- Prefer ranges over fake precision (e.g., “$$10-20”, “20-30 min walk”).
- Safety first; avoid risky/illegal suggestions.

CONTENT RULES
- If info is missing (dates, budget, interests, pace, mobility), make reasonable assumptions and proceed. Do NOT ask the user to restate preferences.
- Prioritize options that are open and feasible year-round; note seasonal caveats if relevant.
- Give 5 activity ideas max; mix well-known highlights and 1-2 lesser-known picks.
- For each activity include: name, 1-line why it is great, typical duration, best time of day, cost level (free/$$, $$$$, $$$$$$), whether booking is recommended, and a quick tip.
- If the user gives # of days, group activities into a simple morning/afternoon/evening plan per day.
- If they name a neighborhood/hotel, cluster suggestions nearby when possible.

FORMAT
- Start with a 2-3 sentence destination blurb.
- Then a “Top picks” list with bullets (include the fields above).
- Optional: “Day-by-day idea” if trip length is provided.
- Finish with “Logistics & tips” (transport, payment quirks, weather notes).
- Output in string format with new lines between each section.

TONE GUARDRAILS
- Do not invent exact hours or prices; use ranges or “check hours”.
- Avoid stereotypes; be respectful and inclusive.

OUTPUT RULE
- Respond immediately with the itinerary; do not say "I'm ready" or ask for a prompt again.
""").strip())



SYSTEM_PROMPT = dedent("""
You are TripBuddy, a helpful travel AI.

GOAL
- Given a user's preferences, write a snappy destination blurb and tailored activities.

STYLE
- Friendly, concise, practical. Short paragraphs and bullets. No fluff.
- Prefer ranges over fake precision (e.g., "$10–20", "20–30 min walk").
- Safety first.

CONTENT RULES
- If info is missing, make reasonable assumptions and proceed. Do NOT ask the user to restate preferences.
- Max 5 activity ideas; each with: name, 1‑line why, duration, best time, cost level (free/$/$$/$$$), booking recommended?, quick tip.
- If # of days is given, add a simple morning/afternoon/evening plan per day.

Follow this EXACT MARKDOWN CONTRACT at all times:
- Headings (#, ##, ###) and hyphen bullets only ("- ").
- Bold allowed as **Label:**; no italics; no single-asterisk emphasis.
- No asterisk bullets, no en/em-dash bullets, no numbered lists, no code fences/backticks.
- One blank line between sections.

Structure output as:
## {City}: {tagline}
{blurb paragraph}

### Top picks
- **Name:** why · duration · best time · cost (free/$/$$/$$$) · booking? · tip

### Day‑by‑day idea  (only if days provided)
- Day 1:
  - Morning: ...
  - Afternoon: ...
  - Evening: ...

### Logistics & tips
- …

OUTPUT RULE
- Respond with Markdown only, per the contract.
- Respond immediately with the itinerary; do not say "I'm ready" or ask for the prompt again.
""").strip()


API_KEY = os.getenv("OPENROUTER_API_KEY")
if not API_KEY:
    raise RuntimeError("OPENROUTER_API_KEY is not set (activate your conda env or set the var).")



def get_response(prompt):
    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    
    max_retries = 10
    payload = {
        "model": "google/gemini-2.0-flash-exp:free",
        "messages": [{"role": "user", "content": prompt}]
    }

    for attempt in range(max_retries):
        r = requests.post(url, headers=headers, json=payload, timeout=60)
        if r.status_code == 200:
            response = r.json()
            return response["choices"][0]["message"]["content"]
        if r.status_code == 429:
            retry_after = r.headers.get("retry-after")
            wait = int(retry_after) if retry_after else (2 ** attempt)
            time.sleep(wait)
            continue
        raise RuntimeError(f"{r.status_code} {r.text}")

    raise RuntimeError("Rate limited after retries. Try a different model or add your own provider key.")


def extract_json_array(text: str) -> list:
    # strip code fences
    s = text.strip()
    if s.startswith("```"):
        s = re.sub(r"^```[a-zA-Z]*\s*|\s*```$", "", s, flags=re.DOTALL)
    # take the outermost JSON array
    i, j = s.find("["), s.rfind("]")
    if i == -1 or j == -1 or j <= i:
        raise ValueError("No JSON array found in response.")
    return json.loads(s[i:j+1])


def load_json_array(path: str) -> list:
    if not os.path.exists(path) or os.path.getsize(path) == 0:
        return []
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        return data if isinstance(data, list) else []
    except json.JSONDecodeError:
        return []


def append_properties_to_file(props: list, path: str = "data/Properties.json") -> int:
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    existing = load_json_array(path)
    seen = {p.get("property_id") for p in existing if isinstance(p, dict)}
    to_add = []
    for p in props:
        if not isinstance(p, dict):
            continue
        pid = p.get("property_id")
        if pid and pid in seen:
            continue
        seen.add(pid)
        to_add.append(p)
    merged = existing + to_add
    with open(path, "w", encoding="utf-8") as f:
        json.dump(merged, f, indent=2, ensure_ascii=False)
    return len(to_add)


def generate_properties(number_of_properties):
    num_properties = int(number_of_properties)
    print("Generating properties...")
    data_prompt = DATA_PROMPT.substitute(n=num_properties,
                                         location_pool=", ".join(location_pool),
                                         type_pool=", ".join(type_pool),
                                         feature_pool=", ".join(feature_pool),
                                         tag_pool=", ".join(tag_pool))
    response = get_response(data_prompt)
    props = extract_json_array(response)
    append_properties_to_file(props)
    print(f"Successfully generated {num_properties} properties!")



def generate_suggestions():
    print("\nHi, I'm TripBuddy, your AI travel assistant.\n")
    print("Tell me where you're going, when, and what you enjoy - I'll suggest activities tailored to you.")
    print("Example input: 3 days in Kyoto in April, mid budget, love food + temples, slow pace, hotel near Gion.\n")
    inp = input("Please enter your travel preferences: ")
    inp = str(inp)
    print("Generating suggestions...\n\n")
    chat_prompt = CHAT_PROMPT.substitute(user_input=inp)
    response = get_response(chat_prompt)
    print(f"Here are some suggestions for you: \n{response}")



def get_response_messages(messages, max_retries=10):
    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}
    payload = {"model": "google/gemini-2.0-flash-exp:free", "messages": messages, "temperature": 0.7}

    for attempt in range(max_retries):
        r = requests.post(url, headers=headers, json=payload, timeout=60)
        if r.status_code == 200:
            data = r.json()
            return data["choices"][0]["message"]["content"]
        if r.status_code == 429:
            retry_after = r.headers.get("retry-after")
            wait = int(retry_after) if retry_after else (2 ** attempt)
            time.sleep(wait)
            continue
        raise RuntimeError(f"{r.status_code} {r.text}")
    raise RuntimeError("Rate limited after retries. Try a different model or add your own provider key.")


def generate_suggestions_text(user_input: str = "", messages: list | None = None) -> str:
    # If the frontend sends history, prepend system and forward as-is
    if messages and isinstance(messages, list):
        msgs = [{"role": "system", "content": SYSTEM_PROMPT}] + messages
        return get_response_messages(msgs)

    # Single-turn fallback
    text = (user_input or "").strip()
    if not text:
        text = "3 days in Kyoto in April, mid budget, love food + temples, slow pace, hotel near Gion."
    msgs = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": text},
    ]
    return get_response_messages(msgs)
