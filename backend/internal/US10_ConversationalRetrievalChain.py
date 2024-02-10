import os
import glob
from langchain.chains import ConversationalRetrievalChain
from US10_initialLLM import initial
from US10_retriever import db

def interactiveBot(query):
    
    llm, memory =initial()
    
    # Ordnerpfad zum Hochladen
    folder = "../interaktion"
    folder_path = glob.glob(os.path.join(folder, "*"))
    
    retriever = db(folder_path)

    bot = ConversationalRetrievalChain.from_llm(
        llm, retriever, memory=memory,verbose=True
    )
    result = bot.invoke({"question": query})

    print(result)




