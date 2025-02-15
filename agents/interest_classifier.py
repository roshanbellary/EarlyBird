from langchain.agents import Tool, AgentExecutor, create_react_agent
from langchain_community.chat_models import ChatOpenAI
from langchain.tools import BaseTool
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.memory import ConversationBufferMemory
from typing import List, Dict
import os
import requests

class InterestClassifierAgent:
    def __init__(self, openai_api_key: str, prompt):
        self.llm = ChatOpenAI(api_key=openai_api_key, model="gpt-3.5-turbo")
        if prompt is None:
            self.prompt = PromptTemplate(
                input_variables=["user_interests"],
                template="""
                Generate a list of 3 topics based on the user's interests below. These topics should be distinct relatively unrelated from eachother:
                {user_interests}
                
                The topics should be outputted as a list of strings.
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