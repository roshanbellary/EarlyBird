from agents.perplexity import PerplexityAPI
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
    def __init__(self, perplexity_api_key: str):
        self.perplexity = PerplexityAPI(perplexity_api_key)
        
    def research_stories(self, headline: str) -> str:
        prompt = f"""
        Conduct deep research on the following news story: {headline}
        Research all current news articles within the past 24-48 hours that provide information related to this topic. 
        Focus specificially on obtaining data regarding expert opinions, related events, statistical data, future implications
        and give specific facts and evidence to support the evidence.
        ONLY OUTPUT THE RELEVANT RESEARCH AND FACTS RELATED TO THE EVENT. DO NOT RETURN ANY OTHER TEXT.
        """
        print(prompt)

        research = self.perplexity.perplexity_query([prompt])
        researched_stories = [{"headline": headline, "research": research}]
        return researched_stories
