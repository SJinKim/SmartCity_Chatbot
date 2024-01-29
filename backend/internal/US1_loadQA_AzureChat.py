import os
import glob
import faiss
import nltk
from tqdm import tqdm
import concurrent.futures
from dotenv import load_dotenv
from langchain_openai import AzureChatOpenAI
from langchain_openai import AzureOpenAIEmbeddings
from langchain_community.docstore import InMemoryDocstore
from langchain.text_splitter import Document, RecursiveCharacterTextSplitter
from langchain_community.document_loaders.unstructured import UnstructuredFileLoader
from langchain_community.vectorstores.faiss import FAISS
from langchain_community.vectorstores.utils import DistanceStrategy
from langchain.chains.question_answering import load_qa_chain
from typing import Any, List

def load_file(file_path:str) -> List[Document]:
    load_dotenv()
    loader = UnstructuredFileLoader(file_path)
    document = loader.load()
    return document


def qa_chain(query) -> Any :
    # Umgebungsvariablen aus env-Datei laden & für Azure OpenAI-API setzen
    load_dotenv()
    os.environ["AZURE_OPENAI_API_KEY"] = os.getenv("AZURE_OPENAI_KEY")
    os.environ["AZURE_OPENAI_ENDPOINT"] = os.getenv("AZURE_OPENAI_ENDPOINT")
    # LLM-Instanz initialisieren
    llm_client = AzureChatOpenAI(
        openai_api_version="2023-10-01-preview",
        azure_deployment="ui-gpt-35-turbo",
        temperature=0.1
    )
    # Embedding-Instanz initialisieren
    embeddings = AzureOpenAIEmbeddings(
        azure_deployment="ui-text-embedding-ada-002",
        model="text-embedding-ada-002",
        api_key=os.getenv("AZURE_OPENAI_KEY"),
        openai_api_version="2023-10-01-preview"
    )

    # Zusatz: Sprachressourcen laden (falls noch nicht heruntergeladen)
    if not nltk.data.find('tokenizers/punkt'):
        nltk.download('punkt') # muss nur 1 Mal ausgeführt werden

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
            progress_bar = tqdm(total=total_files, desc=(f"Dokumente aus Ordner < {folder_name} > werden geladen"))
            futures = [executor.submit(load_document, file_path) for file_path in folder_path]
            for future in concurrent.futures.as_completed(futures):
                doc = future.result()
                docs.extend(doc)
                progress_bar.update(1)
            progress_bar.close()
        #print(f"Anzahl der hochgeladenen Dateien < {len(docs)} > aus Ordner < {folder_name} >")


        # Funktion: Aufteilen der Dokumente in Chunks mit Fortschrittbalken
        def create_text_splitter(documents, max_chunk=2000, min_chunk=400):
            parent_splitter = RecursiveCharacterTextSplitter(chunk_size=max_chunk)
            child_splitter = RecursiveCharacterTextSplitter(chunk_size=min_chunk)
            split_documents = []
            progress = tqdm(total=len(documents),
                            desc=f"{len(documents)} Dokumente werden in Chunk-Größe < {max_chunk} > aufgeteilt")
            for document in documents:
                doc = Document(page_content=document.page_content)
                parent_chunks = parent_splitter.split_documents([doc])
                for parent_chunk in parent_chunks:
                    child_chunks = child_splitter.split_documents([parent_chunk])
                    split_documents.extend(child_chunks)
                progress.update(1)
            progress.close()
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


    # QA-Chain-Prozess:
    # 1.
    chain = load_qa_chain(llm=llm_client, chain_type="stuff", verbose=False)
    """ while True:
        # 2. Nutzeranfrage eingeben
        query = input("Zu was haben Sie eine Frage?\nWenn nicht kann über < exit > der Chat geschlossen werden. ")
        print("--------------------")
        # Zusatz: Chat-Exit durch Eingabe von 'exit'
        if query.lower() == "exit":
            break """

    # Zusatz: Ähnlichkeitssuche auf gespeicherten Vectorstore basierend auf Nutzeranfrage zur Verfeinerung der Suchergebnisse
    results_similar = loaded_faiss_vectorstore.similarity_search(query)
    results_mmr = loaded_faiss_vectorstore.max_marginal_relevance_search(query)
    results_comb = results_similar + results_mmr

    # 3. Antwortgenerierung aus Frage-Antwort-System (mit Fortschrittsbalken)
    with tqdm(total=1, desc="Antwort-Generierung") as pbar:
        response_comb = chain.invoke({"input_documents": results_comb, "question": query}, return_only_outputs=True)
        return str(response_comb['output_text'])

"""         # Zusatz: Antwort übersetzen & formattieren
        translator = GoogleTranslator(source='auto', target='german')
        trans_result = translator.translate(response_comb)
        sentences = nltk.sent_tokenize(trans_result)
        format_response = '\n\n'.join(sentences)
        output = f"[Frage] {query}\n\n[Antwort] {format_response}"
        print(output)
        print("--------------------")
        pbar.update(1) """
