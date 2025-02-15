from langchain.agents import Tool, AgentExecutor, create_react_agent
from langchain_community.chat_models import ChatOpenAI
from langchain.tools import BaseTool
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.memory import ConversationBufferMemory
from typing import List, Dict
import os
import requests

from dotenv import load_dotenv
load_dotenv()

class PerplexityAPI:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://api.perplexity.ai"
    
    def query(self, prompt: str) -> str:
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        data = {
            "model": "sonar",  # or another available model
            "messages": [{"role": "user", "content": prompt}]
        }
        
        response = requests.post(
            f"{self.base_url}/chat/completions",
            headers=headers,
            json=data
        )
        
        if response.status_code == 200:
            return response.json()['choices'][0]['message']['content']
        else:
            raise Exception(f"Error from Perplexity API: {response.text}")

class NewsScraperAgent:
    def __init__(self, perplexity_api_key: str):
        self.perplexity = PerplexityAPI(perplexity_api_key)
        self.prompt = """
        Find the top 5 current news events. For each event, provide:
        1. A brief summary
        2. The main entities involved
        3. The potential impact
        
        Format each event as:
        EVENT 1:
        Summary: [summary]
        Entities: [entities]
        Impact: [impact]
        
        EVENT 2:
        ...
        """
    
    def scrape_news(self) -> List[Dict]:
        response = self.perplexity.query(self.prompt)
        print(response)
        # Parse the response into structured format
        events = []
        current_event = {}
        
        for line in response.split('\n'):
            line = line.strip()
            if line.startswith('## EVENT'):
                if current_event:
                    events.append(current_event)
                current_event = {}
            elif line.startswith('**Summary**:'):
                current_event['summary'] = line[8:].strip()
            elif line.startswith('**Entities**:'):
                current_event['entities'] = line[9:].strip()
            elif line.startswith('**Impact**:'):
                current_event['impact'] = line[7:].strip()
        
        if current_event:
            events.append(current_event)
            
        return events

class HeadlineGeneratorAgent:
    def __init__(self, openai_api_key: str):
        self.llm = ChatOpenAI(api_key=openai_api_key, model="gpt-3.5-turbo")
        self.prompt = PromptTemplate(
            input_variables=["news_item"],
            template="""
            Create an engaging headline for the following news item:
            {news_item}
            
            Make it catchy but informative, suitable for a podcast episode.
            """
        )
        self.chain = LLMChain(llm=self.llm, prompt=self.prompt)
    
    def generate_headlines(self, news_items: List[Dict]) -> List[Dict]:
        headlines = []
        for item in news_items:
            headline = self.chain.run(news_item=str(item))
            headlines.append({**item, "headline": headline})
        return headlines

class DeepResearchAgent:
    def __init__(self, perplexity_api_key: str):
        self.perplexity = PerplexityAPI(perplexity_api_key)
        self.prompt_template = """
        Conduct deep research on the following news story:
        Headline: {headline}
        Summary: {summary}
        
        Provide:
        1. Historical context
        2. Expert opinions
        3. Related events
        4. Statistical data
        5. Future implications
        
        Format your response with clear sections.
        """
    
    def research_stories(self, headlines: List[Dict]) -> List[Dict]:
        researched_stories = []
        for item in headlines:
            prompt = self.prompt_template.format(
                headline=item["headline"],
                summary=item["summary"]
            )
            research = self.perplexity.query(prompt)
            researched_stories.append({**item, "research": research})
        return researched_stories

class StoryDrafterAgent:
    def __init__(self, openai_api_key: str):
        self.llm = ChatOpenAI(api_key=openai_api_key, model="gpt-3.5-turbo")
        self.prompt = PromptTemplate(
            input_variables=["story_data"],
            template="""
            Draft a compelling podcast story based on this research:
            {story_data}
            
            Include:
            1. A hook to grab attention
            2. Clear narrative structure
            3. Key points and analysis
            4. Engaging transitions
            5. Thought-provoking conclusions
            """
        )
        self.chain = LLMChain(llm=self.llm, prompt=self.prompt)
    
    def draft_stories(self, researched_stories: List[Dict]) -> List[Dict]:
        drafted_stories = []
        for story in researched_stories:
            draft = self.chain.run(story_data=str(story))
            drafted_stories.append({**story, "draft": draft})
        return drafted_stories

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

def main():
    # Initialize the pipeline
    print(os.getenv("OPENAI_API_KEY"))
    pipeline = NewsPodcastPipeline(
        perplexity_api_key=os.getenv("PERPLEXITY_API_KEY"),
        openai_api_key=os.getenv("OPENAI_API_KEY")
    )
    
    # Generate podcast scripts
    scripts = pipeline.generate_podcast()
    
    # Save or process the scripts
    for i, script in enumerate(scripts, 1):
        print(f"\n=== Story {i} Script ===\n")
        print(script)
        
        # Optionally save to file
        with open(f"story_{i}_script.txt", "w") as f:
            f.write(script)

if __name__ == "__main__":
    main()