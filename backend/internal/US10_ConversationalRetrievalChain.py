import os
import glob
from langchain.chains import ConversationalRetrievalChain
from US10_initialLLM import initial
from US10_retriever import db

def interactiveBot(query,retriever):
    
    llm, memory =initial()

    bot = ConversationalRetrievalChain.from_llm(
        llm, retriever, memory=memory,verbose=True
    )
    result = bot.invoke({"question": query})

    print(result)




