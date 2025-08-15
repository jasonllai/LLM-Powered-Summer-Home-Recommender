import os
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
- If critical info is missing (dates/season, budget, interests, pace, mobility), ask up to 3 numbered follow-up questions. Otherwise proceed and state any assumptions.
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
""").strip())



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

    
def generate_properties():
    inp = input("The number of properties you want to generate: ")
    if not inp.isdigit():
        print("Please enter a valid number.")
        return
    num_properties = int(inp)
    print("Generating properties...")
    data_prompt = DATA_PROMPT.substitute(n=num_properties,
                                         location_pool=", ".join(location_pool),
                                         type_pool=", ".join(type_pool),
                                         feature_pool=", ".join(feature_pool),
                                         tag_pool=", ".join(tag_pool))
    response = get_response(data_prompt)
    print(f"Successfully generated {num_properties} properties!")
    return response


def generate_suggestions():
    print("Hi, I'm TripBuddy, your AI travel assistant.\n")
    print("Tell me where you're going, when, and what you enjoy - I'll suggest activities tailored to you.\n")
    print("Example input: 3 days in Kyoto in April, mid budget, love food + temples, slow pace, hotel near Gion.\n")
    inp = input("Please enter your travel preferences: ")
    inp = str(inp)
    print("Generating suggestions...")
    chat_prompt = CHAT_PROMPT.substitute(user_input=inp)
    response = get_response(chat_prompt)
    print(f"Here are some suggestions for you: \n{response}")



# print(generate_properties())
# generate_suggestions()



