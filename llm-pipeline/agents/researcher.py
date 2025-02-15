from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, MessagesState, START
from langgraph.prebuilt import create_react_agent

def researcher_node(state: MessagesState) -> MessagesState:
    i = int(config["metadata"]["langgraph_node"][-1])

    researcher_agent = create_react_agent(
        llm=ChatOpenAI(api_key=state["openai_api_key"], model_name="gpt-3.5-turbo"),  # Change to perplexity
        prompt=prompt(state["headlines"][i])
    )
    result = researcher_agent.invoke(state)
    state["research"][i] = result["messages"]
    return state

def prompt(headline: str) -> str:
    return """
    Conduct deep research on the following news story:
    Headline: {headline}
    
    Provide:
    1. Historical context
    2. Expert opinions
    3. Related events
    4. Statistical data
    5. Future implications
    
    Format your response with clear sections.
    """

