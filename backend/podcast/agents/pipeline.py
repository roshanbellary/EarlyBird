from .scraper import NewsScraperAgent
from .researcher import DeepResearchAgent
from .story_drafter import StoryDrafterAgent
from .script_generator import PodcastScriptGenerator
from .interest_classifier import InterestClassifierAgent
from .audio.audio_generation import PodcastAudioGenerator
from langchain.agents import Tool, AgentExecutor, create_react_agent
from langchain_community.chat_models import ChatOpenAI
from langchain.tools import BaseTool
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.memory import ConversationBufferMemory
from typing import List, Dict
import os
import re
import json
from dotenv import load_dotenv

from ml.inference.rl_bandit import HybridLinUCBModel
from ml.retrieval.merger import Article, Merger
# project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
# sys.path.insert(0, project_root)

# from direct.inference.rl_bandit import HybridLinUCBModel
# from direct.retrieval.merger import Article, Merger
# from direct.inference.embed import Embedor


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

        self.articles: list[Article] = Merger(db_path = "backend/podcast/ml/retrieval/db/").merge()
        self.rl_agent = HybridLinUCBModel(articles=self.articles, alpha=1.0, learning_rate=1.0, stabilization=0.001, feedback_exponent=2.0)

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
        # print("Scraping news...")
        # categories = ["Urban Planning", "Beekeeping", "Astrobiology", "Minimalist Living", "Cryptography", "Sumo Wrestling", "Mushroom Foraging", "Antique Restoration"]
        # topic_classifier  = self.interest_classifier.interest_classify(categories)
        # topics = self.parse_topic_classifier(topic_classifier)
        # topics = topics[0:min(len(topics), 3)]
        script = ''
        # news_item = self.scraper.get_top_headlines(topic)
        # print("Generated News Item:", news_item)
        # news_item = self.parse_scraper_response(news_item['content'])

        print("Generating news articles...")
        news_articles: list[Article] = self.rl_agent.return_next_articles(num_articles=5)
        
        for news_item in news_articles:
            print("Conducting deep research...")
            researched_stories = self.researcher.research_stories(news_item.title, news_item.abstract)
            print("Generated Research:")
            research_content = researched_stories[0]["research"]["choices"][0]["message"]["content"]
            # print(f"Drafting story for {news_item.section}...")
            # drafted_stories = self.drafter.draft_stories(researched_stories)
            # self.stories.append({"story": drafted_stories, "topic": news_item.section})
            # print("Stories:", self.stories)

            print(f"Generating script for {news_item.title}...")

            mistral_api_key=os.getenv("MISTRAL_API_KEY")
            self.script_generator = PodcastScriptGenerator(mistral_api_key)
            story = self.script_generator.generate_script(news_item, research_content)     
            script += story   

            print(story)
            
        return script
        # print("Generated Podcast Scripts:", result)
        # return result
    
    # filepath- current audio file playing
    def user_ask_expert(self, question: str, filepath: str) -> str:
        # Use absolute path matching the one in podcast.py
        self.project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
        json_file_path = os.path.join(
            self.project_root,
            'backend',
            'podcast',
            'finished_podcasts',
            'podcast_metadata.json'
        )
        
        # Debug prints
        print(f"Looking for metadata file at: {json_file_path}")
        print(f"Searching for filepath: {filepath}")
        
        with open(json_file_path, "r") as file:
            data = json.load(file)
            # Debug print
            print("Available filepaths in metadata:", [p.get("file_path") for p in data["metadata"]])

        i = int(filepath[filepath.rfind('.mp3') - 1])
        stories = None  # Initialize stories variable
        for podcast in data["metadata"]:
            if filepath in podcast["file_path"]:
                stories = podcast["stories"]
                break
                
        if stories is None:  # Add error handling
            raise ValueError(f"No podcast found with filepath: {filepath}")

        mistral_api_key=os.getenv("MISTRAL_API_KEY")
        script_generator = PodcastScriptGenerator(mistral_api_key)
        script_generator.chat_history.append(f"<HOST{i}>{question}</HOST{i}>")
        ans = script_generator.generate_response(script_generator.expert_chain, stories[i // 2]["story"][0]['draft'])

        # Get the directory from the input filepath
        output_dir = os.path.dirname(filepath)
        audio_generator = PodcastAudioGenerator(output_dir=output_dir)
        interrupt_path = os.path.join(output_dir, f"podcast_interrupt_{i}.mp3")
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

    # Test user_ask_expert
    filepath = "/Users/albert/Documents/coding_projects/EarlyBird/backend/podcast/finished_podcasts/podcast_20250216_001413_3b8ba9c7/interaction_1.mp3"  # Updated filepath
    question = "What are the key points about this topic?"
    result = pipeline.user_ask_expert(question, filepath)
    print(f"Generated interrupt file: {result}")

    # Test generate_podcast
    # pipeline.generate_podcast()