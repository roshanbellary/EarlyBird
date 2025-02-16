from langchain_community.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from typing import Dict, List
import time


class PodcastScriptGenerator:
    def __init__(self, api_key: str):
        # One advanced LLM
        self.advanced_llm = ChatOpenAI(
            model_name="o1-preview",  # or any advanced model you want
            openai_api_key=api_key,
            temperature=1  # Must be 1 for o1-preview
        )

        professional_prompt = """
                You are writing a short, entertaining, and informative podcast script in the style of NPR's "Up First." 
                It must alternate between <HOST> and <EXPERT> tags, like this:

                <HOST>
                [Host speaking...]
                </HOST>
                <EXPERT>
                [Expert speaking...]
                </EXPERT>

                1. Keep it concise, with a clear beginning and ending.
                2. Open with the host greeting and introducing the topic.
                3. The expert offers analysis or answers questions.
                4. Include a final sign-off from the host.

                Below is the story or content you have:
                {stories}

                Now produce the entire script in one pass, following the specified tag format exactly.
            """
        
        structured_prompt =  """ 
                You are writing entertaining, and informative podcast script in the style of NPR's "Up First." 
                It must alternate between <HOSTi> and <EXPERTi> tags, where i is the index of the story. like this:

                <HOST0>
                [Host speaking...]
                </HOST0>
                <EXPERT0>
                [Expert speaking...]
                </EXPERT0>
                <HOST1>
                [Host speaking...]
                </HOST1>
                <EXPERT1>
                [Expert speaking...]
                </EXPERT1>
                ...

                Each story should have two interactions between the host and the expert.
                i.e. <HOST0> <EXPERT0> <HOST1> <EXPERT1> should be about story 1
                <HOST2> <EXPERT2> <HOST3> <EXPERT3> should be about story 2
                <HOST4> <EXPERT4> <HOST5> <EXPERT5> should be about story 3

                <HOST6> should be the final sign-off from the host.

                1. The host should introduce the topic and ask the expert to analyze or answer questions.
                2. Make up names for the host and the expert.
                3. The expert offers analysis or answers questions.
                4. Include a final sign-off from the host.
                5. The questions and responses should be in depth and interesting.
                6. The total script length should be 6-8 minutes. i.e each story should be 2-3 minutes.
                7. Since there are only 6 interactions, it is okay for speakers to speak for longer.
                8. The host should be the same person throughout the script, but the expert should be different for each story.

                Below is the story or content you have:
                {stories}

                Now produce the entire script in one pass, following the specified tag format exactly.
            """

        # Single prompt that generates the entire script
        self.script_generation_prompt = PromptTemplate(
            input_variables=["stories"],
            template=structured_prompt
        )

        # Create LLM chain with o1
        self.script_chain = LLMChain(
            llm=self.advanced_llm, prompt=self.script_generation_prompt, verbose=False
        )

    def generate_script(self, content: List[Dict]) -> str:
        """
        content is a list of dicts, each like:
        {
          "story": [{"draft": "..."}, ...],
          "topic": "..."
        }

        We'll combine all story 'draft's into one text block.
        Then we ask the advanced model to produce a single script with <HOST> and <EXPERT>.
        """
        # Combine everything into one big string
        joined_stories = "\n\n".join(
            story_item["draft"]
            for topic_dict in content
            for story_item in topic_dict["story"]
        )

        # Add a small delay to prevent rate-limiting (optional)
        time.sleep(1)

        # Make one call to get the final script
        script = self.script_chain.run(stories=joined_stories)
        return script
