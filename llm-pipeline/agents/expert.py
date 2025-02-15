from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, MessagesState, START
from langgraph.prebuilt import create_react_agent


def expert_node(state: MessagesState) -> MessagesState:
    i = int(config["metadata"]["langgraph_node"][-1])

    expert_agent = create_react_agent(
        llm=ChatOpenAI(api_key=state["openai_api_key"], model_name="gpt-3.5-turbo"),
        prompt=prompt(state["stories"][i], state["conversations"][i])
    )
    result = expert_agent.invoke(state)
    state["conversations"][i].append(f"EXPERT: {result["messages"]}")
    return state

def prompt(story_data: str, current_story: str) -> str:
    return """
            You are an expert commentator. Respond to the host's comments about this story.
            Here is the story: {story_data}
            Here is the current conversation: {current_story}
            
            Provide insightful analysis and expert perspective.
            """

