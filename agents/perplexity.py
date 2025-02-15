from typing import List, Dict
import requests
class PerplexityAPI:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://api.perplexity.ai"
    
    def query(self, prompt: str) -> str:
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        data = {
            "model": "sonar",  # or another available model
            "messages": [{"role": "user", "content": prompt}]
        }
        
        response = requests.post(
            f"{self.base_url}/chat/completions",
            headers=headers,
            json=data
        )
        
        if response.status_code == 200:
            return response.json()['choices'][0]['message']['content']
        else:
            raise Exception(f"Error from Perplexity API: {response.text}")
    
    def research_stories(self, headlines: List[Dict]) -> List[Dict]:
        researched_stories = []
        for item in headlines:
            prompt = self.prompt_template.format(
                headline=item["headline"],
                summary=item["summary"]
            )
            research = self.perplexity.query(prompt)
            researched_stories.append({**item, "research": research})
        return researched_stories