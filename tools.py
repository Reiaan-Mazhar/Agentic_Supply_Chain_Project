from langchain_core.tools import tool
from pydantic import BaseModel, Field
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings.fastembed import FastEmbedEmbeddings
import os

# 1. Initialize the EXACT same embedding model as ingest_data
embeddings = FastEmbedEmbeddings()
CHROMA_PATH = "./chroma_db"

# 2. Check if DB exists before loading
if os.path.exists(CHROMA_PATH):
    vector_db = Chroma(persist_directory=CHROMA_PATH, embedding_function=embeddings, collection_name="supply_chain_knowledge")
else:
    vector_db = None

class SearchInput(BaseModel):
    query: str = Field(description="The term to search for.")

@tool("search_knowledge_base", args_schema=SearchInput)
def search_knowledge_base(query: str):
    """Searches the company documents for facts."""
    if vector_db is None:
        return "Error: Vector database not found. Please run ingest_data.py first."
    
    # Use k=4 to get more context
    docs = vector_db.similarity_search(query, k=4)
    
    if not docs:
        return f"No matches found for '{query}'. Try a broader query like 'Singapore' or 'SN-202'."
    
    return "\n\n".join([d.page_content for d in docs])

@tool("calculate_risk_score")
def calculate_risk_score(severity: int, inventory_level: int):
    """
    REQUIRED FOR RISK ASSESSMENT. 
    Calculates a numerical risk score (0-100) based on event severity (1-10) 
    and current inventory buffers. High severity and low inventory results in 
    a critical score. Use this only after logistics data is gathered.
    """
    score = (severity * 10) - (inventory_level / 2)
    return f"The calculated risk score is {max(0, min(100, score))}/100."

tools = [search_knowledge_base, calculate_risk_score]