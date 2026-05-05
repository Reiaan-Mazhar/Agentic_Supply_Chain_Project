# persistence_test.py
import sqlite3
from multi_agent_graph import app # Import the compiled app from your main script
from langgraph.checkpoint.sqlite import SqliteSaver

# 1. Reconnect to the database created by the main script
conn = sqlite3.connect("checkpoint_db.sqlite", check_same_thread=False)
memory = SqliteSaver(conn)

# 2. Re-compile (or just use the imported app)
# Use the EXACT same thread_id used in multi_agent_graph.py
config = {"configurable": {"thread_id": "midterm_exam_01"}}

print("--- LAB 5 PERSISTENCE TEST ---")
print("Accessing SQLite Checkpoint Database...")

state = app.get_state(config)

if state.values:
    print("\nSUCCESS: Agent found existing state in SQLite!")
    print(f"Memory Check (Last Message): {state.values['messages'][-1].content[:100]}...")
    print("\nThe agent successfully 'remembered' the conversation across different script runs.")
else:
    print("\nFAILURE: No state found for this thread_id. Run multi_agent_graph.py first.")