from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.memory import ConversationBufferMemory
from typing import Dict, List
import os

class PodcastScriptGenerator:
    def __init__(self, openai_api_key: str, host_prompt: PromptTemplate = None, expert_prompt: PromptTemplate = None):
        # Initialize LLMs for host and expert with different temperatures
        self.host_llm = ChatOpenAI(
            api_key=openai_api_key,
            model="gpt-3.5-turbo",
            temperature=0.7
        )
        
        self.expert_llm = ChatOpenAI(
            api_key=openai_api_key,
            model="gpt-3.5-turbo",
            temperature=0.4
        )
        
        # Modified memory setup to handle combined input
        self.memory = ConversationBufferMemory(
            input_key="combined_input",
            memory_key="chat_history"
        )
        
        # Updated host prompt
        if host_prompt is None:
            self.host_prompt = PromptTemplate(
                input_variables=["combined_input", "chat_history"],
                template="""
                You are a charismatic podcast host discussing an interesting story with an expert panelist.
                
                {combined_input}
                
                Previous Discussion: {chat_history}
                
                Your role is to:
                1. If this is the start, introduce the story engagingly and ask the expert a thought-provoking question
                2. If responding to the expert, acknowledge their points and ask follow-up questions
                3. Keep the conversation natural and flowing
                4. Draw out interesting insights from the expert
                5. Use conversational language while staying professional
                
                Respond in a way that moves the discussion forward naturally.
                """
            )
        else:
            self.host_prompt = host_prompt
        
        # Updated expert prompt
        if expert_prompt is None:
            self.expert_prompt = PromptTemplate(
                input_variables=["combined_input", "chat_history"],
                template="""
                You are a knowledgeable expert panelist on a podcast discussing a story.
                
                {combined_input}
                
                Previous Discussion: {chat_history}
                
                Your role is to:
                1. Provide deep, insightful analysis of the story
                2. Draw from relevant expertise and experience
                3. Respond directly to the host's questions
                4. Add new perspectives and angles to the discussion
                5. Use clear, authoritative language while staying accessible
                
                Respond to the host's latest point or question while advancing the discussion.
                """
            )
        else:
            self.expert_prompt = expert_prompt
        
        # Create LLM chains with updated configuration
        self.host_chain = LLMChain(
            llm=self.host_llm,
            prompt=self.host_prompt,
            memory=self.memory,
            verbose=True
        )
        
        self.expert_chain = LLMChain(
            llm=self.expert_llm,
            prompt=self.expert_prompt,
            memory=self.memory,
            verbose=True
        )

    def generate_script(self, content: str, num_exchanges: int = 4) -> str:
        """
        Generate a podcast script with natural back-and-forth between host and expert.
        
        Args:
            content (str): The story content to be discussed
            num_exchanges (int): Number of back-and-forth exchanges (default: 4)
            
        Returns:
            str: The generated podcast script
        """
        script_segments = []
        chat_history = ""
        
        # Combine content and context into a single input
        combined_input = f"Story Content: {content}\n"
        
        # Initial host introduction and question
        host_intro = self.host_chain.run(combined_input=combined_input)
        script_segments.append(f"HOST: {host_intro}")
        chat_history = host_intro
        
        # Generate conversation back-and-forth
        for _ in range(num_exchanges):
            # Expert response
            expert_response = self.expert_chain.run(
                combined_input=combined_input
            )
            script_segments.append(f"EXPERT: {expert_response}")
            chat_history = f"{chat_history}\nEXPERT: {expert_response}"
            
            # Host follow-up
            host_response = self.host_chain.run(
                combined_input=combined_input
            )
            script_segments.append(f"HOST: {host_response}")
            chat_history = f"{chat_history}\nHOST: {host_response}"
        
        # Add closing remarks
        closing_prompt = PromptTemplate(
            input_variables=["combined_input"],
            template="Provide a brief, natural closing statement for the discussion, thanking the expert."
        )
        closing_chain = LLMChain(llm=self.host_llm, prompt=closing_prompt)
        closing = closing_chain.run(combined_input=combined_input)
        script_segments.append(f"HOST: {closing}")
        
        return "\n\n".join(script_segments)

    def format_script(self, script: str, include_timestamps: bool = True) -> str:
        """
        Format the generated script with optional timestamps and proper spacing.
        
        Args:
            script (str): The raw generated script
            include_timestamps (bool): Whether to include timestamps
            
        Returns:
            str: The formatted script
        """
        formatted_segments = []
        current_time = 0
        
        for segment in script.split("\n\n"):
            if include_timestamps:
                minutes = current_time // 60
                seconds = current_time % 60
                timestamp = f"[{minutes:02d}:{seconds:02d}]"
                formatted_segments.append(f"{timestamp} {segment}")
                current_time += 30  # Approximate 30 seconds per exchange
            else:
                formatted_segments.append(segment)
        
        return "\n\n".join(formatted_segments)