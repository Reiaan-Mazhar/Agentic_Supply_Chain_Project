from multi_agent_graph import app

thread_id = "debug_thread"
config = {"configurable": {"thread_id": thread_id}}
inputs = {"messages": [("user", "What is the risk score for severity 9 and inventory 10?")], "sender": "user"}

print("Starting stream...\n")
for event in app.stream(inputs, config, stream_mode="updates"):
    print("EVENT:")
    for node, data in event.items():
        print(f"  Node: {node}")
        print(f"  Data type: {type(data)}")
        if isinstance(data, dict) and "messages" in data:
            for m in data["messages"]:
                # print structure
                try:
                    content = getattr(m, 'content', None)
                    role = getattr(m, 'role', None) or getattr(m, 'type', None)
                    print(f"    Message role={role!r} content={content!r}")
                except Exception as e:
                    print(f"    Could not introspect message: {e}")
    print("\n")

print("Stream complete.")
