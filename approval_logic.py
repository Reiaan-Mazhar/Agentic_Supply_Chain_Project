# approval_logic.py - Lab 5 Task 2 Documentation
from langgraph.graph import StateGraph
from langgraph.checkpoint.sqlite import SqliteSaver
import sqlite3

# This snippet demonstrates the HITL configuration for the Mid-Exam
def get_approved_graph(workflow, checkpoint_conn):
    memory = SqliteSaver(checkpoint_conn)
    
    # TASK 2: The "Safety Breakpoint" (HITL)
    # We configure the graph to interrupt execution BEFORE the 'action' node.
    # This ensures no tool (Search or Calculate) runs without human approval.
    app = workflow.compile(
        checkpointer=memory, 
        interrupt_before=["action"] 
    )
    return app

print("Technical Specification: interrupt_before=['action'] integrated.")