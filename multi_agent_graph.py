import os
import sqlite3
from typing import Annotated, TypedDict, Literal
from langgraph.graph import StateGraph, END
from langgraph.graph.message import add_messages
from langgraph.checkpoint.sqlite import SqliteSaver
from langgraph.prebuilt import ToolNode
from langchain_groq import ChatGroq
from tools import tools, search_knowledge_base, calculate_risk_score
from dotenv import load_dotenv

load_dotenv()

class AgentState(TypedDict):
    messages: Annotated[list, add_messages]
    sender: str 

# Use a slightly faster model if capacity is an issue, or stick to 70b
llm = ChatGroq(model="llama-3.3-70b-versatile", timeout=30)

# --- NODES ---
def researcher_node(state: AgentState):
    # DONT tell it HOW to use the tool, just give it a goal.
    prompt = "You are a logistics researcher. Find facts about shipments and port status. If found, summarize and say 'HANDOVER'."
    model = llm.bind_tools([search_knowledge_base])
    return {"messages": [model.invoke([{"role": "system", "content": prompt}] + state["messages"])], "sender": "researcher"}

def manager_node(state: AgentState):
    # DONT tell it HOW to use the tool, just give it a goal.
    prompt = "You are a risk manager. Provide a final assessment. Include a numerical risk score if appropriate. End with 'FINAL'."
    model = llm.bind_tools([calculate_risk_score])
    return {"messages": [model.invoke([{"role": "system", "content": prompt}] + state["messages"])], "sender": "manager"}


def router(state: AgentState):
    last_msg = state["messages"][-1]
    # 1. If there's a tool call, always execute it
    if getattr(last_msg, "tool_calls", None):
        return "call_tool"
    # 2. If researcher is done, go to manager
    if state["sender"] == "researcher":
        return "manager"
    # 3. Everything else goes to END (via sanitizer)
    return "end"

workflow = StateGraph(AgentState)
workflow.add_node("researcher", researcher_node)
workflow.add_node("manager", manager_node)
workflow.add_node("call_tool", ToolNode(tools))

workflow.set_entry_point("researcher")

workflow.add_conditional_edges("researcher", router, {"call_tool": "call_tool", "manager": "manager", "end": END})
workflow.add_conditional_edges("manager", router, {"call_tool": "call_tool", "end": END})
workflow.add_conditional_edges("call_tool", lambda x: x["sender"], {"researcher": "researcher", "manager": "manager"})

memory = SqliteSaver(sqlite3.connect("checkpoint_db.sqlite", check_same_thread=False))
# Set a hard recursion limit so it CANNOT loop forever
app = workflow.compile(checkpointer=memory)