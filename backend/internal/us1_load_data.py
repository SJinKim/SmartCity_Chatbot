"""
    Optional (dev-mode): This module contains the function to create a vector index 
    for uploading further data sources (e.g. additional laws) to be added to the project.
"""

import os
import glob
import concurrent.futures

import faiss
from tqdm import tqdm

from dotenv import load_dotenv
from langchain_openai import AzureOpenAIEmbeddings
from langchain_community.vectorstores.faiss import FAISS
from langchain_community.docstore import InMemoryDocstore
from langchain_community.vectorstores.utils import DistanceStrategy
from langchain_community.document_loaders.unstructured import UnstructuredFileLoader
from langchain.text_splitter import Document, RecursiveCharacterTextSplitter

from internal.utils import check_environment


# Retrieves and validates Azure OpenAI API credentials from loaded environment variables.
load_dotenv()
# Raises :ValueError: If either the API key or endpoint is not found in the environment.
check_environment()


def init_embeddings():
    """ Initializes and returns Azure OpenAI Embeddings client.
    Args:   None

    Returns:
        AzureOpenAIEmbeddings: An instance of the Azure OpenAI Embeddings client.
    """
    return AzureOpenAIEmbeddings(
        deployment=os.getenv("AZURE_EMBEDDING_DEPLOYMENT"),
        model=os.getenv("AZURE_EMBEDDING_MODEL"),
        api_key=os.getenv("AZURE_OPENAI_KEY"),
        openai_api_version=os.getenv("AZURE_OPENAI_VERSION"),
    )


embeddings = init_embeddings()


def __load_document(file_path):
    """ Loads a document from a given file path.
    Args:
        file_path (str): The path to the document file.

    Returns:
        Document: The loaded document object.

    Raises:
        IOError: If the file cannot be accessed or loaded.
    """
    loader = UnstructuredFileLoader(file_path)
    document = loader.load()
    return document


def __create_text_splitter(documents, max_chunk=2000, min_chunk=400):
    """ Splits documents into smaller chunks using a recursive approach and
    displays a progress bar.
    Args:
        documents: A list of documents to be split.
        max_chunk: The maximum chunk size for the initial split (default: 2000).
        min_chunk: The minimum chunk size for the recursive split (default: 400).

    Returns:
        A list of split documents.
    """
    parent_splitter = RecursiveCharacterTextSplitter(chunk_size=max_chunk)
    child_splitter = RecursiveCharacterTextSplitter(chunk_size=min_chunk)
    split_documents = []
    progress = tqdm(
        total=len(documents),
        desc=f"{len(documents)} Dokumente werden in Chunk-Größe < {max_chunk} > aufgeteilt",
    )
    for document in documents:
        doc = Document(page_content=document.page_content)
        parent_chunks = parent_splitter.split_documents([doc])
        split_documents.extend(parent_chunks)
        for parent_chunk in parent_chunks:
            child_chunks = child_splitter.split_documents([parent_chunk])
            split_documents.extend(child_chunks)
        progress.update(1)
    progress.close()
    return split_documents


def __create_faiss_index(embedding_func, split_documents):
    """ Creates a vectorestore index, adds the doc chunks to it and saves it to a local file.
    Args:
        embedding_func: The embedding function used to represent documents.
        split_documents: A list of doc chunks to be added to the index.
        index: The name of the order/file to save the index to.

    Returns:    A FAISS vectorstore with the added documents.
    """
    index = faiss.IndexFlatL2(1536)  # System-dimension size
    docstore = InMemoryDocstore(
        {str(i): chunk for i, chunk in enumerate(split_documents)}
    )
    index_to_docstore_id = {i: str(i) for i in range(len(split_documents))}
    distance_strategy = DistanceStrategy.COSINE
    vectorstore_faiss = FAISS(
        embedding_function=embedding_func,
        index=index,
        docstore=docstore,
        index_to_docstore_id=index_to_docstore_id,
        distance_strategy=distance_strategy,
    )
    vectorstore_faiss.add_documents(split_documents)
    return vectorstore_faiss


def __parallel_upload(folder_path, data_folder):
    """ Loads documents in parallel using a thread pool and displays a progress bar.
    Args:
        folder_path (_type_): path to documents folder to be uploaded
        data_folder (_type_): name of the folder to be uploaded

    Returns:
        _type_: _description_
    """
    docs = []
    with concurrent.futures.ThreadPoolExecutor() as executor:
        total_files = len(folder_path)
        progress_bar = tqdm(
            total=total_files,
            desc=(f"Dokumente aus Ordner < {data_folder} > werden geladen"),
        )
        futures = [
            executor.submit(__load_document, file_path) for file_path in folder_path
        ]
        for future in concurrent.futures.as_completed(futures):
            doc = future.result()
            docs.extend(doc)
            progress_bar.update(1)
        progress_bar.close()
    return docs


def upload_data(data_folder, vectorestore_name):
    """ Uploads documents from a data folder to a Vectorstore.
        It checks for a saved index and loads it if available.
        Otherwise, it loads documents in parallel, splits them into chunks,
        creates a FAISS index, and saves it for future use.

    Args:   None

    Returns:    None

    Precondition:   `embeddings` variable is defined.

    Postcondition:  A Vectorstore index containing the uploaded data is available.
    """
    parent_folder = os.path.dirname(os.path.dirname(__file__))
    folder = os.path.join(parent_folder, data_folder)
    folder_path = glob.glob(os.path.join(folder, "*"))

    # Checks for a local index and loads it if available, otherwise creates one.
    local_index = os.path.join(os.path.dirname(__file__), vectorestore_name)
    if os.path.exists(local_index):
        FAISS.load_local(
            folder_path=local_index, embeddings=embeddings, index_name=vectorestore_name
        )
        print("Lokaler Index gefunden & geladen!")
    else:
        print("Kein lokaler Index gefunden, daher wird es erstellt...")
        docs = __parallel_upload(folder_path=folder_path, data_folder=data_folder)
        split_docs = __create_text_splitter(docs)
        print(f"Anzahl der aufgeteilten Chunks: {len(split_docs)}")

        local_vectorestore = __create_faiss_index(embeddings, split_docs)
        index_folder = os.path.join(os.path.dirname(__file__), vectorestore_name)
        local_vectorestore.save_local(
            folder_path=index_folder, index_name=vectorestore_name
        )
        print("Index erstellt und gespeichert!")

        # Loads the saved local Vectorstore index.
        loaded_data = FAISS.load_local(
            folder_path=index_folder,
            embeddings=embeddings,
            index_name=vectorestore_name,
        )
        print("Gespeicherter Index geladen!")
        data_ids = loaded_data.index_to_docstore_id
        print(f"Eingebettete Vektoren im < {vectorestore_name} >: {len(data_ids)}")

# Uncomment the code in order to use the function.
#upload_data(data_folder="Bescheide_docs", vectorestore_name="bescheide_index")
