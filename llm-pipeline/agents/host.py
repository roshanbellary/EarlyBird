from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, MessagesState, START
from langgraph.prebuilt import create_react_agent

def host_node(state: MessagesState) -> MessagesState:
    i = int(config["metadata"]["langgraph_node"][-1])

    host_agent = create_react_agent(
        llm=ChatOpenAI(api_key=state["openai_api_key"], model_name="gpt-3.5-turbo"),
        prompt=prompt(state["stories"][i], state["conversations"][i])
    )
    result = host_agent.invoke(state)
    state["conversations"][i].append(f"HOST: {result["messages"]}")
    state["convo_i"][i] += 1
    return state

def prompt(story_data: str, current_story: str) -> str:
    # Change this prompt based on convo_i (for ex- if convo_i = 0, 
    # then host should introduce the topic, if convo_i = 3, then host 
    # should close out of the topic, otw host should respond to expert and 
    # continue conversation on topic)
    return """
    You are a podcast host. Present this story and respond to the expert's comments:
    Here is the story: {story_data}
    Here is the current conversation: {current_story}
    
    Keep the conversation engaging and natural.
    """

