from langchain.agents import Tool, AgentExecutor, create_react_agent
from langchain_community.chat_models import ChatOpenAI
from langchain.tools import BaseTool
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.memory import ConversationBufferMemory
from typing import List, Dict
import os
import requests

class PodcastScriptGenerator:
    def __init__(self, openai_api_key: str):
        self.expert_llm = ChatOpenAI(api_key=openai_api_key, model="gpt-3.5-turbo")
        self.host_llm = ChatOpenAI(api_key=openai_api_key, model="gpt-3.5-turbo")
        self.memory = ConversationBufferMemory()
        
        self.expert_prompt = PromptTemplate(
            input_variables=["story", "host_comment"],
            template="""
            You are an expert commentator. Respond to the host's comments about this story:
            Story: {story}
            Host: {host_comment}
            
            Provide insightful analysis and expert perspective.
            """
        )
        
        self.host_prompt = PromptTemplate(
            input_variables=["story", "expert_comment"],
            template="""
            You are a podcast host. Present this story and respond to the expert's comments:
            Story: {story}
            Expert: {expert_comment}
            
            Keep the conversation engaging and natural.
            """
        )
        
        self.expert_chain = LLMChain(
            llm=self.expert_llm,
            prompt=self.expert_prompt,
            memory=self.memory
        )
        
        self.host_chain = LLMChain(
            llm=self.host_llm,
            prompt=self.host_prompt,
            memory=self.memory
        )
    
    def generate_script(self, story: Dict) -> str:
        script = []
        
        # Initial host introduction
        host_intro = self.host_chain.run(story=story["draft"], expert_comment="")
        script.append(f"HOST: {host_intro}")
        
        # Generate conversation
        for _ in range(3):  # Number of back-and-forth exchanges
            expert_comment = self.expert_chain.run(
                story=story["draft"],
                host_comment=host_intro
            )
            script.append(f"EXPERT: {expert_comment}")
            
            host_response = self.host_chain.run(
                story=story["draft"],
                expert_comment=expert_comment
            )
            script.append(f"HOST: {host_response}")
            
            host_intro = host_response
        
        return "\n\n".join(script)