from perplexity import PerplexityAPI
from langchain.agents import Tool, AgentExecutor, create_react_agent
from langchain_community.chat_models import ChatOpenAI
from langchain.tools import BaseTool
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.memory import ConversationBufferMemory
from typing import List, Dict
import os
import requests

class NewsScraperAgent:
    def __init__(self, perplexity_api_key: str):
        self.perplexity = PerplexityAPI(perplexity_api_key)

    def get_top_headlines(self, prompt):
        data = self.perplexity.perplexity_query(["List exactly 5 headlines from the last 24 hours related to the user prompt. Format as follows:1. <HEADLINE>[First headline] </HEADLINE> 2. <HEADLINE> [Second headline] </HEADLINE>\n3.<HEADLINE> [Third headline] </HEADLINE>\n4. <HEADLINE>[Fourth headline]<HEADLINE/>\n5. <HEADLINE>[Fifth headline]<HEADLINE/>", prompt])

        if "choices" in data and len(data["choices"]) > 0:
            result = {
                "content": data["choices"][0]["message"]["content"],
                "citations": data.get("citations", [])
            }
            return result
        else:
            print("Unexpected response structure:", data)
            return None