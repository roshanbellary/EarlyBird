from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, MessagesState, START
from langgraph.prebuilt import create_react_agent

def interest_classifier_node(state: MessagesState) -> MessagesState:
    interest_classifier_agent = create_react_agent(
        llm=ChatOpenAI(api_key=state["openai_api_key"], model_name="gpt-3.5-turbo"),
        prompt=prompt(state["user_interests"])
    )
    result = interest_classifier_agent.invoke(state)
    state["story_categories"] = result["messages"]
    return state

def prompt(user_interests: str) -> str:
    return """
    Generate a list of 3 topics based on the user's interests below. These topics should be distinct relatively unrelated from eachother:
    {user_interests}

    The topics should be outputted as a list of strings.
    """

