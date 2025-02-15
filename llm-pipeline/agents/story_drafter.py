from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, MessagesState, START
from langgraph.prebuilt import create_react_agent


def story_drafter_node(state: MessagesState) -> MessagesState:
    i = int(config["metadata"]["langgraph_node"][-1])

    stort_drafter_agent = create_react_agent(
        llm=ChatOpenAI(api_key=state["openai_api_key"], model_name="gpt-3.5-turbo"),
        prompt=prompt(state["research"][i])
    )
    result = stort_drafter_agent.invoke(state)
    state["stories"][i] = result["messages"]
    return state

def prompt(story_data: str) -> str:
    return """
    Draft a compelling podcast story based on this research:
    {story_data}
    
    Include:
    1. A hook to grab attention
    2. Clear narrative structure
    3. Key points and analysis
    4. Engaging transitions
    5. Thought-provoking conclusions
    """

