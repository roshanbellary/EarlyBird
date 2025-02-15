from langchain.agents import Tool, AgentExecutor, create_react_agent
from langchain_community.chat_models import ChatOpenAI
from langchain.tools import BaseTool
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.memory import ConversationBufferMemory
from typing import List, Dict
import os
import requests

class StoryDrafterAgent:
    def __init__(self, openai_api_key: str, prompt: PromptTemplate = None):
        self.llm = ChatOpenAI(api_key=openai_api_key, model="gpt-3.5-turbo")
        if prompt is None:
            self.prompt = PromptTemplate(
                input_variables=["story_data"],
                template="""
                Draft a compelling podcast story based on this research:
                {story_data}
                
                Include:
                1. A hook to grab attention
                2. Clear narrative structure
                3. Key points and analysis
                4. Engaging transitions
                5. Thought-provoking conclusions
                """
            )
        else:
            self.prompt = prompt
        self.chain = LLMChain(llm=self.llm, prompt=self.prompt)
    
    def draft_stories(self, researched_stories: List[Dict]) -> List[Dict]:
        drafted_stories = []
        for story in researched_stories:
            draft = self.chain.run(story_data=str(story))
            drafted_stories.append({**story, "draft": draft})
        return drafted_stories