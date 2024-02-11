import os
from typing import Any, List
from langchain_community.vectorstores.faiss import FAISS
from internal.US1_splitter import create_text_splitter
from internal.US1_parallelupload import parallelUpload
from internal.US1_create_faissindex import create_faiss_index

def loadData(data_path,embeddings,indexName):
    
    # leere Liste für geladene Dokumente
    docs = []

    # Prüfung, ob gespeicherter Vectorstore existiert
    if os.path.exists("./"+indexName):
        # Ja: gespeicherter Vectorestore wird geladen
        loaded_faiss_vectorstore = FAISS.load_local("./internal/"+indexName, embeddings)
        print("Index available and successfully loaded")
    else:
        docs = parallelUpload(data_path, docs)
        split_docs, child_splitter = create_text_splitter(docs)
        faiss_vectorstore = create_faiss_index(embeddings, split_docs)
        #print("Index created")  

        # Funktion: Lokales Speichern des erstellten Vectorstores, um als Index zu nutzen
        def save_index(vector_store, filename):
            vector_store.save_local(filename)

        save_index(faiss_vectorstore, indexName)
        print("Index saved")  # Test
        
        # gespeicherten Index laden
        loaded_faiss_vectorstore = FAISS.load_local(indexName, embeddings)
        print("Index loaded")  # Test
        
        # Anzahl der Chunk-IDs im Index prüfen
        num_chunk_ids = loaded_faiss_vectorstore.index_to_docstore_id
        #print(f"< {len(num_chunk_ids)} > Chunk-IDs wurden im erstellen FAISS-Vectorstore gespeichert")
    
    return loaded_faiss_vectorstore 
        
