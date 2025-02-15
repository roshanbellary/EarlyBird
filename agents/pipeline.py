from scraper import NewsScraperAgent
from headline_gen import HeadlineGeneratorAgent
from researcher import DeepResearchAgent
from story_drafter import StoryDrafterAgent
from script_generator import PodcastScriptGenerator

from langchain.agents import Tool, AgentExecutor, create_react_agent
from langchain_community.chat_models import ChatOpenAI
from langchain.tools import BaseTool
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.memory import ConversationBufferMemory
from typing import List, Dict
import os
from dotenv import load_dotenv
load_dotenv()

class NewsPodcastPipeline:
    def __init__(
        self,
        perplexity_api_key: str,
        openai_api_key: str
    ):
        self.scraper = NewsScraperAgent(perplexity_api_key)
        self.headline_generator = HeadlineGeneratorAgent(openai_api_key)
        self.researcher = DeepResearchAgent(perplexity_api_key)
        self.drafter = StoryDrafterAgent(openai_api_key)
        self.script_generator = PodcastScriptGenerator(openai_api_key)
    
    def generate_podcast(self) -> List[str]:
        # Execute the pipeline
        print("Scraping news...")
        news_items = self.scraper.scrape_news()
        print("News Items:", news_items)
        print("Generating headlines...")
        headlines = self.headline_generator.generate_headlines(news_items)
        print("Generated Headlines:", headlines)
        print("Conducting deep research...")
        researched_stories = self.researcher.research_stories(headlines)
        
        print("Drafting stories...")
        drafted_stories = self.drafter.draft_stories(researched_stories)
        
        print("Generating scripts...")
        # Generate scripts for each story
        scripts = []
        for story in drafted_stories:
            script = self.script_generator.generate_script(story)
            scripts.append(script)
        
        return scripts

if __name__ == "__main__":
    # Initialize the pipeline
    print(os.getenv("OPENAI_API_KEY"))
    pipeline = NewsPodcastPipeline(
        perplexity_api_key=os.getenv("PERPLEXITY_API_KEY"),
        openai_api_key=os.getenv("OPENAI_API_KEY"))
    pipeline.generate_podcast()