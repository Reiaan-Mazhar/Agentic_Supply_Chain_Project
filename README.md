# Agentic Supply Chain Risk Mitigation Agent

This project is a multi-agent system built using **LangGraph**, **Groq (Llama 3.3)**, and **ChromaDB**.

## Features
- **RAG Integration:** Uses FastEmbed to ground agent reasoning in private contract PDFs.
- **Autonomous Reasoning:** Implements a ReAct loop to decide when to search data or calculate risk.
- **Tools:** Custom Python tools for risk scoring and database retrieval.

## Setup
1. Install dependencies: `pip install -r requirements.txt`
2. Add your `GROQ_API_KEY` to a `.env` file.
3. Run `python ingest_data.py` to initialize the knowledge base.
4. Run `python graph.py` to start the agent.