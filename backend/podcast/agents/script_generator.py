from langchain_community.chat_models import ChatOpenAI
from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.memory import ConversationBufferWindowMemory
from typing import Dict, List
import os
import time

class PodcastScriptGenerator:
    def __init__(self, mistral_api_key: str):
        # Initialize LLMs for host and expert with different temperatures
        self.host_llm = ChatOpenAI(
            model_name="mistral-tiny",
            openai_api_base="https://api.mistral.ai/v1",
            openai_api_key=mistral_api_key
        )

        self.expert_llm = ChatOpenAI(
            model_name="mistral-tiny",
            openai_api_base="https://api.mistral.ai/v1",
            openai_api_key=mistral_api_key
        )
        
        # Use window memory to limit context size
        self.memory = ConversationBufferWindowMemory(
            k=4,  # Only keep last 2 exchanges
            input_key="combined_input",
            memory_key="chat_history"
        )
        
        # Updated host prompt
        self.host_prompt = PromptTemplate(
            input_variables=["combined_input", "chat_history"],
            template="""
            You are a charismatic podcast host discussing an interesting story with an expert panelist.
            
            {combined_input}
            
            Previous Discussion: {chat_history}
            
            Your role is to:
            1. If responding to the expert, ask follow-up questions
            2. Keep the conversation natural and flowing
            3. Draw out interesting insights from the expert
            4. Use conversational language while staying professional
            5. Remember that you are a host and speaking to an audience as well as the expert
            
            Respond in a way that moves the discussion forward naturally. Refer to the expert as Dr. Bellary.
            ONLY INCLUDE YOUR RESPONSE. DO NOT PUT 'Host: ' AT THE BEGINNING OF THE LINE. DO NOT INCLUDE ANY PREVOUS CONTEXT. DO NOT REENACT THE EXPERT. YOU ARE THE HOST AND ONLY THE HOST.
            KEEP YOUR RESPONSE TO TWO OR THREE LINES. DO NOT NAME THE PODCAST. THIS IS YOUR ONE AND ONLY SHOT IF YOU GET THIS WRONG I WILL CUT OFF MY ARM.
            """
        )
        
        # Updated expert prompt
        self.expert_prompt = PromptTemplate(
            input_variables=["combined_input", "chat_history"],
            template="""
            You are a knowledgeable expert panelist named Dr. Bellary on a podcast discussing a story.
            
            {combined_input}
            
            Previous Discussion: {chat_history}
            
            Your role is to:
            1. Provide deep, insightful analysis of the story
            2. Draw from relevant expertise and experience
            3. Respond directly to the host's questions
            4. Add new perspectives and angles to the discussion
            5. Use clear, authoritative language while staying accessible
            6. Include very specific examples and facts from the story.
            
            Respond to the host's latest point or question while advancing the discussion.
            ONLY INCLUDE YOUR RESPONSE DO NOT REPEAT ANY CONTEXT GIVEN
            DO NOT REENACT THE HOST. DO NOT PUT 'Dr. Bellary' AT BEGINNING OF THE LINE. YOU ARE THE EXPERT AND ONLY THE EXPERT.
            KEEP YOUR RESPONSE TO TWO OR THREE LINES. THIS IS YOUR ONE AND ONLY SHOT 
            IF YOU GET THIS WRONG I WILL CUT OFF MY ARM.
            """
        )
        
        # Create LLM chains with updated configuration
        self.host_chain = LLMChain(
            llm=self.host_llm,
            prompt=self.host_prompt,
            memory=self.memory,
            verbose=False
        )
        
        self.expert_chain = LLMChain(
            llm=self.expert_llm,
            prompt=self.expert_prompt,
            memory=self.memory,
            verbose=False
        )

    def generate_response(self, chain, combined_input: str) -> str:
        """
        Generate a response with basic rate limiting
        """
        # Add small delay to prevent rate limiting
        time.sleep(1)
        return chain.run(combined_input=combined_input)

    def generate_script(self, content: List[Dict]) -> str:
        script_segments = []
        # print("content:", content)

        for i in range(len(content)):
            # print(content[i]['story'])
            for j in range(2):     
                print(content[i]['topic'], j)           
                # Ensure smooth transitions between topics
                if j == 0:
                    if i == 0:
                        combined_input = f"""
                            Give a 1 sentence brief and broad introduction to the podcast welcoming the audience and the expert. Then, introduce the attached story. Here is the story: {content[i]['story']}
                        """
                    else:
                        combined_input = f"""
                            Now, make a 1 sentence transition to the next story in the form 'Thank you for your perspective, now we will switch to a different story'. Then introduce the new story. YOU MUST BEGIN TALKING ABOUT THE NEW STORY AND TOPIC AND STOP TALKING ABOUT THE PREVIOUS STORY. IF YOU DO NOT I WILL KILL MYSELF. Here is the story: {content[i]['story']}
                        """
                else:
                    combined_input = f"""
                        DO NOT REINTRODUCE THE EXPERT OR THE AUDIENCE TO THE SHOW
                        Here is the store: {content[i]['story']}
                    """
                print(combined_input)

                # if i > 0:
                #     transition_text = f"""
                #     Previously, we discussed {content[i-1]['topic']}. Now, let's transition to our next topic: {content[i]['topic']}.
                #     """
                #     combined_input = transition_text + "\n" + combined_input

                # Host's introduction to the new topic
                host_intro = self.generate_response(self.host_chain, combined_input)
                script_segments.append(f"<HOST>{host_intro}</HOST>")

                # Expert's response to the host
                expert_response = self.generate_response(self.expert_chain, combined_input)
                script_segments.append(f"<EXPERT>{expert_response}</EXPERT>")

                # Add a wrap-up statement at the end
                if i == len(content) - 1 and j == 1:
                    closing_prompt = PromptTemplate(
                        input_variables=["combined_input"],
                        template="""
                        Provide a brief 1 sentence closing statement to wrap up the podcast, thanking the expert and audience.
                        """
                    )
                    closing_chain = LLMChain(llm=self.host_llm, prompt=closing_prompt)
                    closing = self.generate_response(closing_chain, combined_input)
                    script_segments.append(f"<HOST>{closing}</HOST>")

        return "\n\n".join(script_segments)

