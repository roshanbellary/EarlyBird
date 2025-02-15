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

def get_detailed_report(prompt):
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
                "content": "You are a news analyst. Focus on analyzing the SINGLE news story provided in the prompt. Provide a detailed breakdown including: 1) Core story details 2) Background context 3) Key implications 4) Latest developments. Do NOT list other headlines or stories."
                # "content": "Provide a comprehensive analysis of the specified news story. Include key details, background context, implications, and latest developments. Be thorough but well-organized."
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        "max_tokens": 1000,
        "temperature": 0.1  # Lower temperature for more focused responses
    }

    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        data = response.json()
        
        if "choices" in data and len(data["choices"]) > 0:
            return {
                "content": data["choices"][0]["message"]["content"],
                "citations": data.get("citations", [])
            }
    except (requests.exceptions.RequestException, ValueError) as err:
        print(f"Error: {err}")
        return None

    return None

if __name__ == "__main__":
    if len(sys.argv) < 1:
        print("Usage: python content_retrieval_agent.py '<topic>'")
        sys.exit(1)

    prompt = sys.argv[1]

    # First get headlines
    print("\nFetching top headlines...")
    headlines_response = get_top_headlines(prompt)
    
    if headlines_response:
        print("\nTop Headlines:")
        print(headlines_response["content"])
        print("\nSources:")
        for citation in headlines_response["citations"]:
            print("-", citation)
        
        # Extract the first bullet point as the top headline
        headlines_lines = [line.strip() for line in headlines_response["content"].split("\n") if line.strip()]
        first_bullet = next((line[3:] for line in headlines_lines if line.startswith("1. ")), "")
        if not first_bullet:
            # Fallback to using the 3rd non-header line if bullets aren't found
            first_bullet = headlines_lines[2] if len(headlines_lines) >= 3 else ""
        
        print("\nFetching detailed report on top story...")
        print("Getting detailed report on:", first_bullet)
        detailed_response = get_detailed_report(first_bullet)
        
        if detailed_response:
            print("\nDetailed Report:")
            print(detailed_response["content"])
            print("\nSources:")
            for citation in detailed_response["citations"]:
                print("-", citation)
    else:
        print("No response received.")