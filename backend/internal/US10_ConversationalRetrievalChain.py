
from langchain.chains import ConversationalRetrievalChain
from internal.US10_initialLLM import initial
from internal.US10_retriever import db

def interactiveBot(query,retriever):
    
    llm, embeddings,memory =initial()

    bot = ConversationalRetrievalChain.from_llm(
        llm, retriever, memory=memory,verbose=True
    )
    result = bot.invoke({"question": query})
    return result




