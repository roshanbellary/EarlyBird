#!/usr/bin/env python3
import os
import sys
import requests
from dotenv import load_dotenv

load_dotenv()

PERPLEXITY_API_KEY = os.getenv("PERPLEXITY_KEY")
if not PERPLEXITY_API_KEY:
    print("PERPLEXITY_API_KEY not found in environment variables. Please check your .env file.")
    sys.exit(1)

def get_chat_response(prompt):
    url = "https://api.perplexity.ai/chat/completions"
    headers = {
        "Authorization": f"Bearer {PERPLEXITY_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "sonar-pro",
        "messages": [
            {
                "role": "system", 
                "content": "Find me the top 5 headlines from the last 24 hours related to the user prompt"
            },
            {
                "role": "user", 
            "content": prompt
            }
        ],
        "max_tokens": 500,
        # return images is an option
    }

    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
    except requests.exceptions.RequestException as err:
        print("Error fetching data:", err)
        return None

    try:
        data = response.json()
    except ValueError as err:
        print("Error parsing JSON:", err)
        return None

    if "choices" in data and len(data["choices"]) > 0:
        result = {
            "content": data["choices"][0]["message"]["content"],
            "citations": data.get("citations", [])
        }
        return result
    else:
        print("Unexpected response structure:", data)
        return None

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python updated_script.py '<prompt>'")
        sys.exit(1)

    prompt = sys.argv[1]
    response = get_chat_response(prompt)
    if response:
        print("Content:", response["content"])
        print("\nSources:")
        for citation in response["citations"]:
            print("-", citation)
    else:
        print("No response received.")