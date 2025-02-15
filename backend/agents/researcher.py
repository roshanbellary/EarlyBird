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

class DeepResearchAgent:
    def __init__(self, perplexity_api_key: str, prompt: str = None):
        self.perplexity = PerplexityAPI(perplexity_api_key)
        self.prompt_template = """
        Conduct deep research on the following news story:
        Headline: {headline}
        
        Provide:
        1. Historical context
        2. Expert opinions
        3. Related events
        4. Statistical data
        5. Future implications
        
        Format your response with clear sections.
        """
    def research_stories(self, headline: str) -> str:
        researched_stories = []
        prompt = self.prompt_template.format(
            headline=headline
        )
        research = self.perplexity.perplexity_query(prompt)
        researched_stories.append({"headline": headline, "research": research})
        return researched_stories
