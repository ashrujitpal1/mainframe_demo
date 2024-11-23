from langgraph.graph import MessagesState
from langchain_community import END
from typing import Literal
from typing_extensions import TypedDict
from langchain_ollama import OllamaLLM as Ollama

class AgentState(MessagesState):
    next: str


members = ["generation", "review"]
options = members + ["FINISH"]

system_prompt = (
    "You are a supervisor tasked with managing a conversation between the"
    " following workers:  {members}. Given the following user request,"
    " respond with the worker to act next. Each worker will perform a"
    " task and respond with their results and status. When finished,"
    " respond with FINISH." 
)

class Router(TypedDict):
    """Worked to route to next. If no workers needed, route to FINISH"""
    next: Literal[*options]

llm = Ollama(model="ollama/llama3.2", base_url="http://localhost:11434")

def supervisor_node(state: AgentState) -> AgentState:
    """Router to decide which worker to route to next"""
    messages = [
        {
            "role": "system",
            "content": system_prompt
        },
    ] + state["messages"]
    response = llm.with_structured_output(Router).invoke(messages)
    next_ = response["next"]
    if next_ == "FINISH":
        next_ = END

    return {
        "next": next_,
        "messages": messages,
    }