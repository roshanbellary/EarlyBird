#!/usr/bin/env python3
import os
import sys
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("API_KEY")
if not API_KEY:
    print("API_KEY not found in environment variables. Please check your .env file.")
    sys.exit(1)

def get_chat_response(prompt):
    url = "https://api.perplexity.ai/chat/completions"
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "sonar",
        "messages": [
            {"role": "system", "content": "Be precise and concise."},
            {"role": "user", "content": prompt}
        ],
        "max_tokens": 200,
        "temperature": 0.2,
        "top_p": 0.9,
        "top_k": 0,
        "stream": False,
        "presence_penalty": 0,
        "frequency_penalty": 1
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
        return data["choices"][0]["message"]["content"]
    else:
        print("Unexpected response structure:", data)
        return None

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python updated_script.py '<prompt>'")
        sys.exit(1)

    prompt = sys.argv[1]
    response_text = get_chat_response(prompt)
    if response_text:
        print(response_text)
    else:
        print("No response received.")