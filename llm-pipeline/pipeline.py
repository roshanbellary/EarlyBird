from langchain_core.runnables import RunnableConfig
from typing_extensions import Annotated, TypedDict
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import StateGraph, MessagesState, START

from agents.interest_classifier import interest_classifier_node
from agents.headline_generator import headline_generator_node
from agents.researcher import researcher_node
from agents.story_drafter import story_drafter_node
from agents.host import host_node
from agents.expert import expert_node

import os
from dotenv import load_dotenv
load_dotenv()

class State(TypedDict):
    user_interests: str
    story_categories: list[str]
    headlines: list[str]
    research: list[str]
    stories: list[str]
    conversations: list[list[str]]
    convo_i: list[int] # What step of conversation the expert/host is on
    perplexity_api_key: str
    openai_api_key: str

graph = StateGraph(State)

graph.add_node("interest_classifier", interest_classifier_node)
for i in range(3):
    graph.add_node(f"headline_generator_{i}", headline_generator_node)
    graph.add_node(f"researcher_{i}", researcher_node)
    graph.add_node(f"story_drafter_{i}", story_drafter_node)
    graph.add_node(f"host_{i}", host_node)
    graph.add_node(f"expert_{i}", expert_node)

def host_route(state: State):
    i = int(config["metadata"]["langgraph_node"][-1])
    if state["convo_i"][i] < 4:
        return "expert_node"
    else:
        return END

graph.set_entry_point("interest_classifier")
for i in range(3):
    graph.add_edge("interest_classifier", f"headline_generator_{i}")
    graph.add_edge(f"headline_generator_{i}", f"researcher_{i}")
    graph.add_edge(f"researcher_{i}", f"story_drafter_{i}")
    graph.add_edge(f"story_drafter_{i}", f"host_{i}")
    graph.add_conditional_edges(f"host_{i}", host_route)
    graph.add_edge(f"expert_{i}", f"host_{i}")

initial_state = {"user_interests": "I enjoy Latest technology news, Global political headlines, and Recent sports updates", 
                "story_categories": ['', '', ''], "headlines": ['', '', ''], "research": ['', '', ''], "stories": ['', '', ''], 
                "conversations": [[], [], []], "i": 0, "convo_i": [0, 0, 0], "perplexity_api_key": os.getenv("PERPLEXITY_API_KEY"), 
                "openai_api_key": os.getenv("OPENAI_API_KEY")}
compiled = graph.compile()
final_state = compiled.invoke(initial_state)
print(final_state)

