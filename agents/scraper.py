from perplexity import PerplexityAPI
from langchain.agents import Tool, AgentExecutor, create_react_agent
from langchain_community.chat_models import ChatOpenAI
from langchain.tools import BaseTool
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.memory import ConversationBufferMemory
from typing import List, Dict
import os
import requests

class NewsScraperAgent:
    def __init__(self, perplexity_api_key: str):
        self.perplexity = PerplexityAPI(perplexity_api_key)
        self.prompt = """
        Find the top 5 current news events. For each event, provide:
        1. A brief summary
        2. The main entities involved
        3. The potential impact
        
        Format each event as:
        EVENT 1:
        Summary: [summary]
        Entities: [entities]
        Impact: [impact]
        
        EVENT 2:
        ...
        """
    
    def scrape_news(self) -> List[Dict]:
        response = self.perplexity.query(self.prompt)
        print(response)
        # Parse the response into structured format
        events = []
        current_event = {}
        
        for line in response.split('\n'):
            line = line.strip()
            if line.startswith('## EVENT'):
                if current_event:
                    events.append(current_event)
                current_event = {}
            elif line.startswith('**Summary**:'):
                current_event['summary'] = line[8:].strip()
            elif line.startswith('**Entities**:'):
                current_event['entities'] = line[9:].strip()
            elif line.startswith('**Impact**:'):
                current_event['impact'] = line[7:].strip()
        
        if current_event:
            events.append(current_event)
            
        return events