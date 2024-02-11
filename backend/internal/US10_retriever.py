import os,glob
from internal.US1_loadData import loadData
from internal.US10_initialLLM import initial
from langchain_community.vectorstores.faiss import FAISS

def db(folder)->FAISS:
   
    embeddings=initial()[1]
    
    folder_path = glob.glob(os.path.join(folder, "*"))
    print(folder_path)
    indexName= os.path.basename(folder)
    print(indexName)
    db = loadData(folder_path,embeddings,indexName)
    print("fertig db")

    retriever = db.as_retriever()
    return retriever