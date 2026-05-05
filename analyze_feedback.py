import sqlite3
import json
from langchain_groq import ChatGroq
from dotenv import load_dotenv

load_dotenv()

DB_PATH = "feedback_log.db"

def get_negative_feedback():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT user_input, agent_response, optional_comment FROM feedback WHERE feedback_score = -1")
    rows = cursor.fetchall()
    conn.close()
    return rows

def analyze():
    rows = get_negative_feedback()
    if not rows:
        print("No negative feedback to analyze.")
        return
        
    llm = ChatGroq(model="llama-3.3-70b-versatile")
    
    prompt = f"""
    You are a Drift Monitor. Analyze the following negative feedback records.
    Categorize the primary failures (e.g., 'Hallucination', 'Wrong Tool', 'Tone').
    Provide a 1-paragraph summary of your findings.
    
    Feedback Records:
    {json.dumps(rows, indent=2)}
    """
    
    response = llm.invoke([{"role": "user", "content": prompt}])
    print("--- Drift Analysis Report ---")
    print(response.content)

if __name__ == "__main__":
    # Seed the database with mock bad feedback for demonstration if empty
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS feedback (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            thread_id TEXT,
            user_input TEXT,
            agent_response TEXT,
            feedback_score INTEGER,
            optional_comment TEXT)''')
    
    cursor.execute("SELECT COUNT(*) FROM feedback")
    if cursor.fetchone()[0] == 0:
        mock_data = [
            ("2026-05-01T12:00:00", "t1", "Can you reset my password?", "The calculated risk score is 10/100.", -1, "Wrong tool used, I am asking about passwords."),
            ("2026-05-02T12:00:00", "t2", "What is my email?", "The calculated risk score is 0.", -1, "Agent is ignoring out-of-scope instructions instead of politely declining.")
        ]
        cursor.executemany("INSERT INTO feedback (timestamp, thread_id, user_input, agent_response, feedback_score, optional_comment) VALUES (?, ?, ?, ?, ?, ?)", mock_data)
        conn.commit()
    conn.close()
    
    analyze()
