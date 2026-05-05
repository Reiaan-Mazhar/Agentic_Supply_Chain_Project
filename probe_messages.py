import langchain_core
from langchain_core import messages
print('module:', messages)
print([n for n in dir(messages) if 'Message' in n or 'AI' in n or 'Human' in n][:200])
# try common constructors
for name in ('AIMessage','HumanMessage','ai_message','human_message','system_message'):
    print(name, hasattr(messages, name))
