from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, MessagesState, START
from langgraph.prebuilt import create_react_agent

def headline_generator_node(state: MessagesState, config: dict) -> MessagesState:
    i = int(config["metadata"]["langgraph_node"][-1])
    headline_generator_agent = create_react_agent (
        llm=ChatOpenAI(api_key=state["openai_api_key"], model_name="gpt-3.5-turbo"),  # Change to perplexity
        prompt=prompt(state["story_categories"][i])
    )

    result = headline_generator_agent.invoke(state)
    state["headlines"][i] = result["messages"]
    return state

def prompt(story_category: str) -> str:
    return """
    Create an engaging headline for the following news item:
    {story_category}
    
    Make it catchy but informative, suitable for a podcast episode.
    """

