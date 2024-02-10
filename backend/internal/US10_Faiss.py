from langchain.text_splitter import CharacterTextSplitter
from langchain_community.document_loaders import TextLoader
from langchain_community.vectorstores.faiss import FAISS
from langchain_openai import OpenAIEmbeddings
from dotenv import load_dotenv
import os
from langchain_community.document_loaders import DirectoryLoader
from backend.internal.US1_loadData import init_embeddings, uploadData
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

""" loader = DirectoryLoader('../interaktionDB/', glob="**/*.{pdf,docx}")
documents  = loader.load()
text_splitter = CharacterTextSplitter(chunk_size=500, chunk_overlap=20)

docs = text_splitter.split_documents(documents) """
""" embeddings = init_embeddings()

db = FAISS.from_documents(docs, embeddings) """

""" query = "Fass den ganzen Sachverhalt in einem Satz innerhalb 50 Wörter. "
docs = db.similarity_search(query) """
""" print(docs) """


folder_path = "../interaktionDB/"

embeddings = init_embeddings()
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



embeddings = init_embeddings()
uploadData("../interaktionDB/", "interaktionDB",emb = embeddings )


""" documents =load_document("./interaktionDB/")
docs =split_documents(documents)
embeddings = init_embeddings()
db = FAISS.from_documents(docs, embeddings) """


