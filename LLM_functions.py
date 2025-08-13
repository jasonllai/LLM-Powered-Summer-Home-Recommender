import requests
import json
import os



def get_response(prompt):
    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer <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>",  # f"Bearer {os.getenv('OPENROUTER_API_KEY')}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "google/gemini-2.0-flash-exp:free",
        "messages": [{"role": "user", "content": prompt}]
    }
    response = requests.post(url, headers=headers, data=json.dumps(data))
    return response.json()["choices"][0]["message"]["content"]
    
def generate_properties(num_properties):
    prompt = f"Generate {num_properties} properties for a summer home rental website. Each property should have a unique property_id, location, type, price_per_night, features, and tags. The properties should be in Canada. The properties should be in the following types: {property_types}. The properties should be in the following locations: {locations}. The properties should have the following features: {features}. The properties should have the following tags: {tags}."
    response = get_response(prompt)
    return response


def generate_suggestions(user_input):
    prompt = f"Generate travel blurbs, suggested activities based on the user's input: {user_input}. The suggestions should be in the following format: {suggestion_format}. The suggestions should be in the following locations: {locations}. The suggestions should have the following features: {features}. The suggestions should have the following tags: {tags}."
    response = get_response(prompt)
    return response