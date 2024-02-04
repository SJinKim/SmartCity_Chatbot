import os
import glob
import faiss
import concurrent.futures
from typing import Any, List
from dotenv import load_dotenv
from langchain_community.vectorstores.faiss import FAISS
from langchain_community.docstore import InMemoryDocstore
from langchain_openai import AzureOpenAIEmbeddings
from langchain_community.vectorstores.utils import DistanceStrategy
from langchain.text_splitter import Document, RecursiveCharacterTextSplitter
from langchain_community.document_loaders.unstructured import UnstructuredFileLoader



load_dotenv()
api_key = os.getenv("AZURE_OPENAI_KEY")
if not api_key:
    raise ValueError("< API Key > nicht gefunden!")
azure_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
if not azure_endpoint:
    raise ValueError("< API Endpoint > nicht gefunden!")



def init_embeddings():   
   return AzureOpenAIEmbeddings(
        deployment=os.getenv("AZURE_EMBEDDING_DEPLOYMENT"),
        model=os.getenv("AZURE_EMBEDDING_MODEL"),
        api_key=api_key,
        openai_api_version=os.getenv("AZURE_OPENAI_VERSION")
   )

embeddings = init_embeddings()


def load_file(file_path:str) -> List[Document]:
    loader = UnstructuredFileLoader(file_path)
    document = loader.load()
    return document


def uploadData() -> Any :
    # Ordnerpfad zum Hochladen
    folder = "../Data"
    folder_path = glob.glob(os.path.join(folder, "*"))
    folder_name = os.path.basename(folder)
    # leere Liste für geladene Dokumente
    docs = []


    # Funktion: Dokument aus bestimmten Dateipfad laden
    def load_document(file_path):
        loader = UnstructuredFileLoader(file_path)
        document = loader.load()
        return document

    # Prüfung, ob gespeicherter Vectorstore existiert
    if os.path.exists("./internal/data_recursive"):
        # Ja: gespeicherter Vectorestore wird geladen
        loaded_faiss_vectorstore = FAISS.load_local("./internal/data_recursive", embeddings)
    else:
        # Sonst: Dokumente aus geg. Ordnerpfad werden parallel geladen (mit Fortschrittsbalken)
        with concurrent.futures.ThreadPoolExecutor() as executor:
            total_files = len(folder_path)
            futures = [executor.submit(load_document, file_path) for file_path in folder_path]
            for future in concurrent.futures.as_completed(futures):
                doc = future.result()
                docs.extend(doc)
        #print(f"Anzahl der hochgeladenen Dateien < {len(docs)} > aus Ordner < {folder_name} >")


        # Funktion: Aufteilen der Dokumente in Chunks mit Fortschrittbalken
        def create_text_splitter(documents, max_chunk=2000, min_chunk=400):
            parent_splitter = RecursiveCharacterTextSplitter(chunk_size=max_chunk)
            child_splitter = RecursiveCharacterTextSplitter(chunk_size=min_chunk)
            split_documents = []
            for document in documents:
                doc = Document(page_content=document.page_content)
                parent_chunks = parent_splitter.split_documents([doc])
                for parent_chunk in parent_chunks:
                    child_chunks = child_splitter.split_documents([parent_chunk])
                    split_documents.extend(child_chunks)
            #print(f"Anzahl der aufgeteilten Chunks < {len(split_documents)} > mit max. Chunk-Größe < {max_chunk} >")
            return split_documents, child_splitter

        split_docs, child_splitter = create_text_splitter(docs)
        #print(f"Anzahl der aufgeteilten Chunks: {len(split_docs)}")  # Test
        #print(f"Größe der Chunks (min_chunk): {child_splitter._chunk_size}")  # Test


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

        faiss_vectorstore = create_faiss_index(embeddings, split_docs)
        #print("Index created")  # Test


        # Funktion: Lokales Speichern des erstellten Vectorstores, um als Index zu nutzen
        def save_index(vector_store, filename):
            vector_store.save_local(filename)

        save_index(faiss_vectorstore, "data_recursive")
        print("Index saved")  # Test
        # gespeicherten Index laden
        loaded_faiss_vectorstore = FAISS.load_local("data_recursive", embeddings)
        print("Index loaded")  # Test
        # Anzahl der Chunk-IDs im Index prüfen
        num_chunk_ids = loaded_faiss_vectorstore.index_to_docstore_id
        #print(f"< {len(num_chunk_ids)} > Chunk-IDs wurden im erstellen FAISS-Vectorstore gespeichert")
        
uploadData()