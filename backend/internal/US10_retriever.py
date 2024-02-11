import os,glob
from internal.US1_loadData import loadData
from internal.US10_initialLLM import initial
from langchain_community.vectorstores.faiss import FAISS

def db(folder)->FAISS:
    
    embeddings=initial()[1]
    
    folder_path = glob.glob(os.path.join(folder, "*"))
    indexName= os.path.basename(folder)
    db = loadData(folder_path,embeddings,indexName)

    retriever = db.as_retriever()
    return retriever