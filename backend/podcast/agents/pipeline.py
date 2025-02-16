from .scraper import NewsScraperAgent
from .researcher import DeepResearchAgent
from .story_drafter import StoryDrafterAgent
from .script_generator import PodcastScriptGenerator
from .interest_classifier import InterestClassifierAgent
from agents.audio.audio_generation import PodcastAudioGenerator, generate_interrupt_response
from langchain.agents import Tool, AgentExecutor, create_react_agent
from langchain_community.chat_models import ChatOpenAI
from langchain.tools import BaseTool
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.memory import ConversationBufferMemory
from typing import List, Dict
import os
import re
from dotenv import load_dotenv
load_dotenv()

class NewsPodcastPipeline:
    def __init__(
        self,
        perplexity_api_key: str,
        openai_api_key: str,
        mistral_api_key: str
    ):
        self.scraper = NewsScraperAgent(perplexity_api_key)
        self.interest_classifier = InterestClassifierAgent(openai_api_key)
        self.researcher = DeepResearchAgent(perplexity_api_key)
        self.drafter = StoryDrafterAgent(openai_api_key)
        self.stories = []
    def parse_topic_classifier(self, response: str) -> List[str]:
        topics = re.findall(r"<TOPIC>(.*?)</TOPIC>", response, re.DOTALL)
        return topics
    def parse_scraper_response(self, response: str) -> List[str]:
        # Parse the response into structured format
        headlines = re.findall(r"<HEADLINE>(.*?)</HEADLINE>", response, re.DOTALL)
        list_of_headlines = [headline.strip() for headline in headlines]
        print(list_of_headlines)
        return list_of_headlines[0]
    def parse_research_stories(self, response: List[Dict]) -> List[Dict]:
        result = []
        for story in response:
            parsed_story = {}
            parsed_story["headline"] = story["headline"]
            parsed_story["content"] = story["choices"][0]["message"]["content"]
            result.append(parsed_story)
        return result
    def generate_podcast(self) -> str:
        # Execute the pipeline
        print("Scraping news...")
        categories = ["Urban Planning", "Beekeeping", "Astrobiology", "Minimalist Living", "Cryptography", "Sumo Wrestling", "Mushroom Foraging", "Antique Restoration"]
        topic_classifier  = self.interest_classifier.interest_classify(categories)
        topics = self.parse_topic_classifier(topic_classifier)
        topics = topics[0:min(len(topics), 3)]
        print("Generated Topics:", topics)
        script = ''
        for topic in topics:
            news_item = self.scraper.get_top_headlines(topic)
            print("Generated News Item:", news_item)
            news_item = self.parse_scraper_response(news_item['content'])

            print("Conducting deep research...")
            researched_stories = self.researcher.research_stories(news_item)
            print("Generated Research:", researched_stories)

            print(f"Drafting story for {topic}...")
            drafted_stories = self.drafter.draft_stories(researched_stories)
            self.stories.append({"story": drafted_stories, "topic": topic})
            print("Stories:", self.stories)

            print(f"Generating script for {topic}...")

            mistral_api_key=os.getenv("MISTRAL_API_KEY")
            self.script_generator = PodcastScriptGenerator(mistral_api_key)
            story = self.script_generator.generate_script(self.stories)     
            script += story   
            print('\n' + script)

        print(script)
        
        return script
        # print("Generated Podcast Scripts:", result)
        # return result
    
    # filepath- current audio file playing
    def user_ask_expert(question: str, filepath: str) -> str:
        i = int(filepath[filepath.rfind('.mp3') - 1])
        mistral_api_key=os.getenv("MISTRAL_API_KEY")
        self.script_generator = PodcastScriptGenerator(mistral_api_key)
        self.script_generator.chat_history.append(f"<HOST{i}>{question}</HOST{i}>")
        ans = self.script_generator.generate_response(self.script_generator.expert_chain, stories[i / 2]["story"][0]['draft'])

        audio_generator = PodcastAudioGenerator()
        interrupt_path = filepath[:filepath.rfind('\\')] + '\\' + 'podcast_interrupt_' + str(i) + '.mp3'
        audio_generator.generate_interrupt_response(ans, interrupt_path)
        return interrupt_path



if __name__ == "__main__":
    # Initialize the pipeline
    print(os.getenv("OPENAI_API_KEY"))
    pipeline = NewsPodcastPipeline(
        perplexity_api_key=os.getenv("PERPLEXITY_API_KEY"),
        openai_api_key=os.getenv("OPENAI_API_KEY"),
        mistral_api_key=os.getenv("MISTRAL_API_KEY")
    )
    pipeline.generate_podcast()