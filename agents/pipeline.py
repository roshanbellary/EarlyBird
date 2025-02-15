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
import re
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
    def parse_scraper_response(self, response: str) -> List[str]:
        # Parse the response into structured format
        headlines = re.findall(r"<HEADLINE>(.*?)</HEADLINE>", response, re.DOTALL)
        list_of_headlines = [headline.strip() for headline in headlines]
        return list_of_headlines[0:min(5, len(list_of_headlines))]
    def parse_research_stories(self, response: List[Dict]) -> List[Dict]:
        result = []
        for story in response:
            parsed_story = {}
            parsed_story["headline"] = story["headline"]
            parsed_story["content"] = story["choices"][0]["message"]["content"]
            result.append(parsed_story)
        return result
    def parse_story_scripts(self, response: List[Dict]) -> List[Dict]:
        result = []
        for story in response:
            parsed_story = {}
            parsed_story["headline"] = story["headline"]
            parsed_story["content"] = story["draft"]
            result.append(parsed_story)
        return result
        
    def generate_podcast(self) -> None:
        # Execute the pipeline
        print("Scraping news...")
        categories = ["politics", "technology", "business"]
        prompt = "Here are the categories the user is interested in:".format(", ".join(categories))
        news_items = self.scraper.get_top_headlines(prompt=prompt)
        news_items = self.parse_scraper_response(news_items['content'])
        print("Generating headlines...")
        headlines = self.headline_generator.generate_headlines(news_items)
        print("Generated Headlines:", headlines)
        print("Conducting deep research...")
        researched_stories = self.researcher.research_stories(headlines)
        print("Generated Research:", researched_stories)
        print("Drafting stories...")
        drafted_stories = self.drafter.draft_stories(researched_stories)
        print("Drafted Stories:", drafted_stories)
        print("Generating scripts...")
        drafted_stories = self.parse_story_scripts(drafted_stories)
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