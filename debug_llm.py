import os
from dotenv import load_dotenv
load_dotenv()
print('GROQ_API_KEY (env):', os.getenv('GROQ_API_KEY'))

try:
    from langchain_groq import ChatGroq
    llm = ChatGroq(model="llama-3.3-70b-versatile")
    print('ChatGroq object created:', type(llm))
    # attempt a dry invoke; wrap to avoid long waits
    try:
        resp = llm.invoke([{"role":"system","content":"Say hi."}])
        print('LLM invoke returned:', resp)
    except Exception as e:
        print('LLM invoke error:', repr(e))
except Exception as e:
    print('Import/Create ChatGroq failed:', repr(e))
