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
    def __init__(self, perplexity_api_key: str):
        self.perplexity = PerplexityAPI(perplexity_api_key)
        
<<<<<<< HEAD
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
=======
        Provide:
        1. Historical context
        2. Expert opinions
        3. Related events
        4. Statistical data
        5. Future implications
        
        Format your response with clear sections.
        """
    def research_stories(self, headline: str) -> List[Dict]:
        researched_stories = []
        prompt = self.prompt_template.format(
            headline=headline
        )
        research = self.perplexity.perplexity_query(prompt)
        researched_stories.append({"headline": headline, "research": research})
>>>>>>> 34de9a86a215a0859216fa611cbf66dcc2628582
        return researched_stories
