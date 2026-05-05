import streamlit as st
import requests
import sqlite3
import uuid
from datetime import datetime

DB_PATH = "feedback_log.db"
API_URL = "http://127.0.0.1:8000/chat"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS feedback (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            thread_id TEXT,
            user_input TEXT,
            agent_response TEXT,
            feedback_score INTEGER,
            optional_comment TEXT
        )
    ''')
    conn.commit()
    conn.close()

init_db()

st.title("Agentic Supply Chain Explorer")

if "thread_id" not in st.session_state:
    st.session_state.thread_id = str(uuid.uuid4())
if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if prompt := st.chat_input("What is your supply chain query?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
        
    try:
        response = requests.post(API_URL, json={"message": prompt, "thread_id": st.session_state.thread_id})
        if response.status_code == 200:
            answer = response.json().get("answer", "Error retrieving response.")
        else:
            answer = "Failed to connect to API."
    except Exception as e:
        answer = f"API Connection Error: {e}"
        
    st.session_state.messages.append({"role": "assistant", "content": answer})
    with st.chat_message("assistant"):
        st.markdown(answer)
        
    st.rerun()

# Feedback Mechanism for the last response
if len(st.session_state.messages) >= 2:
    st.write("**Rate the agent's response:**")
    col1, col2, col3 = st.columns([1, 1, 4])
    
    with col1:
        if st.button("👍"):
            conn = sqlite3.connect(DB_PATH)
            conn.cursor().execute("INSERT INTO feedback (timestamp, thread_id, user_input, agent_response, feedback_score, optional_comment) VALUES (?, ?, ?, ?, ?, ?)", 
                (datetime.now().isoformat(), st.session_state.thread_id, st.session_state.messages[-2]["content"], st.session_state.messages[-1]["content"], 1, ""))
            conn.commit()
            conn.close()
            st.success("Feedback saved!")
            
    with col2:
        if st.button("👎"):
            st.session_state.show_comment = True
            
    if st.session_state.get("show_comment"):
        comment = st.text_input("Why was this bad?")
        if st.button("Submit Comment"):
            conn = sqlite3.connect(DB_PATH)
            conn.cursor().execute("INSERT INTO feedback (timestamp, thread_id, user_input, agent_response, feedback_score, optional_comment) VALUES (?, ?, ?, ?, ?, ?)", 
                (datetime.now().isoformat(), st.session_state.thread_id, st.session_state.messages[-2]["content"], st.session_state.messages[-1]["content"], -1, comment))
            conn.commit()
            conn.close()
            st.session_state.show_comment = False
            st.success("Negative feedback saved!")
