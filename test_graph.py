import os
from dotenv import load_dotenv
from multi_agent_graph import app as agent_app

load_dotenv()

config = {"configurable": {"thread_id": "test_id_123"}}
inputs = {"messages": [("user", "test question")]}
result = agent_app.invoke(inputs, config)

print("RESULT KEYS:", result.keys())
print("MESSAGES:")
if "messages" in result:
    for m in result["messages"]:
        print(type(m), m)
else:
    print("No messages in result!")
