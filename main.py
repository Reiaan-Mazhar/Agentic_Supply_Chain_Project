import os
from fastapi import FastAPI, HTTPException
from schema import ChatRequest, ChatResponse
from multi_agent_graph import app as agent_app

app = FastAPI(title="Agentic Supply Chain API", version="1.0")

@app.get("/")
def root():
    return {"status": "Agent API is running."}

@app.post("/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    try:
        config = {"configurable": {"thread_id": request.thread_id}}
        inputs = {"messages": [("user", request.message)]}
        
        # Run the agent until it reaches END
        result = agent_app.invoke(inputs, config)
        
        # FIX: Find the last message that has actual text content
        final_answer = None
        if "messages" in result:
            # Look backwards through messages for the first one with text
            for msg in reversed(result["messages"]):
                if msg.content and len(msg.content.strip()) > 0:
                    # Ensure it's not just a tool call message
                    if not getattr(msg, "tool_calls", None):
                        final_answer = msg.content
                        break
        
        if final_answer:
            return ChatResponse(status="success", answer=final_answer)
        else:
            return ChatResponse(status="error", error="Agent failed to generate a text summary.")
            
    except Exception as e:
        print(f"CRITICAL ERROR: {str(e)}")
        return ChatResponse(status="error", error=str(e))