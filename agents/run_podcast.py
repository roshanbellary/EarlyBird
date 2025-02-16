from langchain.agents import Tool, AgentExecutor, create_react_agent
from langchain_community.chat_models import ChatOpenAI
from langchain.tools import BaseTool
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.memory import ConversationBufferMemory
from typing import List, Dict
import os
import requests

from pipeline import NewsPodcastPipeline

from dotenv import load_dotenv
load_dotenv()

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
