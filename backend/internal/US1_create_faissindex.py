import faiss
from langchain_community.vectorstores.faiss import FAISS
from langchain_community.docstore import InMemoryDocstore
from langchain_community.vectorstores.utils import DistanceStrategy


# Funktion: Vectorstores erstellen durch Embedding der Dokumenten-Chunks
def create_faiss_index(embedding_func, split_documents):
    index = faiss.IndexFlatL2(1536)  # System-Dimension: 1536
    docstore = InMemoryDocstore({str(i): chunk for i, chunk in enumerate(split_documents)})
    index_to_docstore_id = {i: str(i) for i in range(len(split_documents))}
    distance_strategy = DistanceStrategy.COSINE
    vectorstore_faiss = FAISS(embedding_function=embedding_func, index=index, docstore=docstore,
                            index_to_docstore_id=index_to_docstore_id, distance_strategy=distance_strategy)
    vectorstore_faiss.add_documents(split_documents)
    return vectorstore_faiss