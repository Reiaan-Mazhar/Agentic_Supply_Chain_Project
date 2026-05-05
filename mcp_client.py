# Part B: Task 2 - MCP Client Interaction Pipeline
import os
import json
from dotenv import load_dotenv
from mcp_server import mcp_server # Separate module import
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, ToolMessage

load_dotenv()

# --- 1. MODEL LAYER ---
model = ChatGroq(model="llama-3.3-70b-versatile")

def run_mcp_pipeline(user_prompt: str):
    print(f"\n[CLIENT]: User Query: {user_prompt}")
    
    # --- 2. CONTEXT LAYER: Tool Discovery via MCP Protocol ---
    # The client 'asks' the server what it can do
    discovery_response = mcp_server.handle_discovery()
    available_tools = discovery_response["tools"]
    print("[CLIENT]: Discovered MCP Tools:")
    print(json.dumps(available_tools, indent=2))
    
    # Transform MCP schema into LangChain format for the LLM
    llm_tools = []
    for name, schema in available_tools.items():
        llm_tools.append({
            "name": name,
            "description": schema["description"],
            "parameters": schema["parameters"]
        })
    
    # Bind discovered tools to the model
    model_with_tools = model.bind_tools(llm_tools)
    
    # --- 3. EXECUTION LAYER: LLM Reasoning ---
    print("[CLIENT]: Sending discovered context to LLM...")
    ai_msg = model_with_tools.invoke([HumanMessage(content=user_prompt)])
    
    # Check if the LLM wants to use an MCP tool
    if ai_msg.tool_calls:
        for tool_call in ai_msg.tool_calls:
            t_name = tool_call["name"]
            t_args = tool_call["args"]
            
            print(f"[CLIENT]: LLM decided to use MCP Tool: {t_name}")
            
            # --- PROTOCOL CALL: Execution via MCP rather than direct function call ---
            # We send a 'request' to the server handle
            mcp_response = mcp_server.handle_call(t_name, t_args)
            
            # --- 4. RESPONSE HANDLING ---
            print(f"[CLIENT]: Received MCP Response: {json.dumps(mcp_response, indent=2)}")
            
            # Final synthesis by the LLM
            final_resp = model.invoke([
                HumanMessage(content=user_prompt), 
                ai_msg, 
                ToolMessage(content=json.dumps(mcp_response), tool_call_id=tool_call["id"])
            ])
            print(f"\n[FINAL OUTPUT]: {final_resp.content}")
    else:
        print(f"\n[FINAL OUTPUT]: {ai_msg.content}")

if __name__ == "__main__":
    # Test case demonstrating tool decision by model
    run_mcp_pipeline("I need to ship 15kg to Singapore. What is the rate?")