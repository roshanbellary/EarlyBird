from langchain.agents import Tool, AgentExecutor, create_react_agent
from langchain_community.chat_models import ChatOpenAI
from langchain.tools import BaseTool
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.memory import ConversationBufferMemory
from typing import List, Dict
import os
import requests

class HeadlineGeneratorAgent:
    def __init__(self, openai_api_key: str):
        self.llm = ChatOpenAI(api_key=openai_api_key, model="gpt-3.5-turbo")
        self.prompt = PromptTemplate(
            input_variables=["news_item"],
            template="""
            Create an engaging headline for the following news item:
            {news_item}
            
            Make it catchy but informative, suitable for a podcast episode.
            """
        )
        self.chain = LLMChain(llm=self.llm, prompt=self.prompt)
    
    def generate_headlines(self, news_items: List[str]) -> List[Dict]:
        headlines = []
        for item in news_items:
            headline = self.chain.run(news_item=item)
            headlines.append({"headline": headline, "summary": item})
        return headlines