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
            openai_api_key=mistral_api_key,
        )

        self.expert_llm = ChatOpenAI(
            model_name="mistral-tiny",
            openai_api_base="https://api.mistral.ai/v1",
            openai_api_key=mistral_api_key,
        )

        self.chat_history = []

        # Updated host prompt
        self.host_prompt = PromptTemplate(
            input_variables=["combined_input", "chat_history"],
            template="""
            You are a charismatic podcast host discussing an interesting story with an expert panelist.
            
            {combined_input}
            
            Previous Discussion: {chat_history}
            
            Your role is to:
            1. Respond to the expert in a few words and ask follow up questions regarding the information in the story to continue the conversation
            2. Keep the conversation natural and flowing
            3. Use conversational language while staying professional
            4. Remember that you are a host and speaking to an audience as well as the expert
            
            Respond in a way that moves the discussion forward naturally.
            ONLY INCLUDE YOUR RESPONSE. YOU MUST LIMIT RESPONSES TO 1-2 SENTENCES. DO NOT PUT 'Host: ' AT THE BEGINNING OF THE LINE. DO NOT INCLUDE ANY PREVOUS CONTEXT. DO NOT REENACT THE EXPERT. YOU ARE THE HOST AND ONLY THE HOST.
            DO NOT NAME THE PODCAST. DO NOT REFER TO THE EXPERT AS 'EXPERT' OR 'DR. BELLARY'. THIS IS YOUR ONE AND ONLY SHOT IF YOU BREAK ONE OF THESE RULES I WILL CUT OFF MY ARM.
            """,
        )

        # Updated expert prompt
        self.expert_prompt = PromptTemplate(
            input_variables=["combined_input", "chat_history"],
            template="""
            You are a knowledgeable expert panelist named Dr. Bellary on a podcast discussing a story.
            
            {combined_input}
            
            Previous Discussion: {chat_history}
            
            Your role is to:
            1. Provide deep, insightful, concise analysis of the story
            2. Draw from relevant expertise and experience
            3. Respond directly to the host's questions
            4. Add new perspectives and angles to the discussion
            5. Use clear, authoritative language while staying accessible
            6. Include very specific examples and facts from the story.
            
            Respond to the host's latest point or question while advancing the discussion.
            ONLY INCLUDE YOUR RESPONSE DO NOT REPEAT ANY CONTEXT GIVEN. YOU MUST LIMIT RESPONSES TO 1-2 SENTENCES.
            DO NOT REENACT THE HOST. DO NOT PUT 'Dr. Bellary' AT BEGINNING OF THE LINE. YOU ARE THE EXPERT AND ONLY THE EXPERT.
            KEEP YOUR RESPONSE TO TWO OR THREE LINES. THIS IS YOUR ONE AND ONLY SHOT 
            IF YOU DO BREAK ONE OF THESE RULES I WILL CUT OFF MY ARM.
            """,
        )

        # Create LLM chains with updated configuration
        self.host_chain = LLMChain(
            llm=self.host_llm,
            prompt=self.host_prompt,
            verbose=False,
        )

        self.expert_chain = LLMChain(
            llm=self.expert_llm,
            prompt=self.expert_prompt,
            verbose=False,
        )

    def generate_response(self, chain, combined_input: str) -> str:
        """
        Generate a response with basic rate limiting
        """
        # Add small delay to prevent rate limiting
        time.sleep(1)
        return chain.run(combined_input=combined_input, chat_history=self.chat_history)

    def generate_script(self, content: List[Dict]) -> str:
        print(content)
        story_text = content[-1]["story"][0]['draft']

        for j in range(2):
            if j == 0:
                if len(content) == 1:
                    combined_input = f"""
                        You must give a brief 1 sentence introduction to the podcast welcoming the host and the audience. 
                        Then, give a 1 sentence introduction to the attached story in a headline format. YOU MUST FOLLOW THIS INTRODUCTION FORMAT.
                        Here is the story: {story_text}
                    """
                else:
                    combined_input = f"""
                        Now, give a 1 sentence transition to the new story in the form 'thank you for your input. now moving on to a new topic I would love to hear your opinion on the new story'. 
                        Ensure the transition is very vague because you do not have context on the previous story. YOU MUST FOLLOW THIS TRANSITION FORMAT.
                        Here is the story: {story_text}
                    """
            else:
                combined_input = f"""
                    Here is the story: {story_text}
                """

            # print(combined_input)

            i = 2 * (len(content) - 1) + j
            # Host's introduction/response
            host_intro = self.generate_response(self.host_chain, combined_input)
            self.chat_history.append(f"<HOST{i}>{host_intro}</HOST{i}>")

            # Expert's response using the story text
            expert_response = self.generate_response(self.expert_chain, story_text)
            self.chat_history.append(f"<EXPERT{i}>{expert_response}</EXPERT{i}>")

        if len(content) == 3:
            # Add final closing statement
            if len(content) > 0:
                closing_prompt = PromptTemplate(
                    input_variables=["combined_input"],
                    template="""
                            Provide a brief 1 sentence closing statement to wrap up the podcast, thanking the expert and audience.
                            """,
                )
                closing_chain = LLMChain(llm=self.host_llm, prompt=closing_prompt)
                closing = self.generate_response(closing_chain, combined_input)
                self.chat_history.append(f"<HOST{6}>{closing}</HOST{6}>")

        return "\n\n".join(self.chat_history)
