from langgraph.graph import StateGraph,START,END
from typing import TypedDict
from groq import Groq
import os
from dotenv import load_dotenv
from google.adk.models.lite_llm import LiteLlm
from litellm import acompletion

load_dotenv()
os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY")

class GraphState(TypedDict):
    """Represents the state of the graph."""
    input :str
    output: str

async def llm_node(state:GraphState):
    response = await acompletion(
        model = "groq/qwen/qwen3-32b",
        messages =[
            {"role":"user","content":state["input"]}
        ]
    )
    return {"output": response.choices[0].message.content}


def create_graph():

    graph = StateGraph(GraphState)
    graph.add_node("llm_node", llm_node)

    graph.add_edge(START, "llm_node")
    graph.add_edge("llm_node", END)

    graph_compiler = graph.compile()
    return graph_compiler






