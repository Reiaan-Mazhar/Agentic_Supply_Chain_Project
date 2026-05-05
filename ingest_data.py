import os
from dotenv import load_dotenv
load_dotenv()

from langchain_community.document_loaders import DirectoryLoader, PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings.fastembed import FastEmbedEmbeddings

DATA_PATH = "./data"
CHROMA_PATH = "./chroma_db"

# --- 1. PASTE THE FUNCTION HERE ---
def get_metadata(file_path):
    """Lab 2 Task 1: Metadata Enrichment - Attach 3 searchable tags"""
    filename = os.path.basename(file_path).lower()
    
    # Tag 1: Document Type
    doc_type = "Contract" if "sla" in filename or "agreement" in filename else "SOP"
    
    # Tag 2: Department 
    dept = "Legal/Procurement" if doc_type == "Contract" else "Logistics/Operations"
    
    # Tag 3: Priority Level (Requirement: last_updated or priority)
    priority = "High" if doc_type == "Contract" else "Medium"
    
    return {
        "doc_type": doc_type,
        "department": dept,
        "priority_level": priority,
        "source": filename
    }

def process_documents():
    print("--- Starting RAG Ingestion Pipeline ---")
    
    # 2. Load Documents
    loader = DirectoryLoader(DATA_PATH, glob="**/*.pdf", loader_cls=PyPDFLoader)
    raw_docs = loader.load()
    
    # --- 3. CALL THE FUNCTION HERE ---
    # We update the metadata of each document BEFORE we split it into chunks
    for doc in raw_docs:
        # Clean text (Lab 2 Requirement: Strip whitespace)
        doc.page_content = " ".join(doc.page_content.split())
        
        # Apply the 3 metadata tags
        new_metadata = get_metadata(doc.metadata.get('source', 'unknown'))
        doc.metadata.update(new_metadata)

    # 4. Semantic Chunking (Lab 2 Task 2)
    # Smaller chunks ensure the metadata is highly relevant to the specific text
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=300, chunk_overlap=30)
    chunks = text_splitter.split_documents(raw_docs)
     
    print(f"Success: Created {len(chunks)} chunks with 3+ metadata tags each.")

    # 5. Vector Indexing (Lab 2 Task 3)
    embeddings = FastEmbedEmbeddings()
    vector_db = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=CHROMA_PATH,
        collection_name="supply_chain_knowledge"
    )
    print(f"Vector Database saved to {CHROMA_PATH}")

if __name__ == "__main__":
    import shutil
    if os.path.exists(CHROMA_PATH):
        shutil.rmtree(CHROMA_PATH)
    process_documents()