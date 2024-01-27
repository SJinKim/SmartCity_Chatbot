import os
import glob
import faiss
import nltk
from tqdm import tqdm
import concurrent.futures
from dotenv import load_dotenv
from langchain_community.chat_models import AzureChatOpenAI
from langchain_community.embeddings import AzureOpenAIEmbeddings
from deep_translator import GoogleTranslator
from langchain_community.docstore import InMemoryDocstore
from langchain.text_splitter import Document, RecursiveCharacterTextSplitter
from langchain_community.document_loaders.unstructured import UnstructuredFileLoader
from langchain_community.vectorstores.faiss import FAISS
from langchain_community.vectorstores.utils import DistanceStrategy
from langchain.chains import RetrievalQA

def re_qa_chain(query) -> str :
    # Umgebungsvariablen aus env-Datei laden & für Azure OpenAI-API setzen
    load_dotenv()
    os.environ["AZURE_OPENAI_API_KEY"] = os.getenv("AZURE_OPENAI_KEY")
    os.environ["AZURE_OPENAI_ENDPOINT"] = os.getenv("AZURE_OPENAI_ENDPOINT")
    # LLM-Instanz initialisieren
    llm_client = AzureChatOpenAI(
        openai_api_version="2023-10-01-preview",
        azure_deployment="ui-gpt-35-turbo",
        temperature=0.0
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
        nltk.download('punkt') # muss nur 1 Mal geladen werden

    # Ordnerpfad zum Hochladen
    folder = "Data"
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
    if os.path.exists("data_recursive"):
        # Ja: gespeicherter Vectorestore wird geladen
        loaded_faiss_vectorstore = FAISS.load_local("data_recursive", embeddings)
        print("found index")
        # Optional: Indexe im gespeicherten Vectorestore prüfen
        index_path = os.path.join("data_recursive", "index.faiss")
        path_name = os.path.basename(r"/Demo/data_recursive")
        index = faiss.read_index(index_path)
        anzahl_indexe = index.ntotal
        # print(f"< {anzahl_indexe} > Indexe in FAISS-Vectorestore < {path_name} >")
    else:
        print("index not found")
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
        print(f"Anzahl der hochgeladenen Dateien < {len(docs)} > aus Ordner < {folder_name} >")


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
            print(f"Anzahl der aufgeteilten Chunks < {len(split_documents)} > mit max. Chunk-Größe < {max_chunk} >")
            return split_documents, child_splitter

        split_docs, child_splitter = create_text_splitter(docs)
        print(f"Anzahl der aufgeteilten Chunks: {len(split_docs)}")  # Test
        print(f"Größe der Chunks (min_chunk): {child_splitter._chunk_size}")  # Test

        # Funktion: Vectorstore erstellen durch Embedding der Dokumenten-Chunks
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
        print("Index created")  # Test


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
        print(f"< {len(num_chunk_ids)} > Chunk-IDs wurden im erstellen FAISS-Vectorstore gespeichert")


    # RetrievalQA-Prozess:
    # 1. RetrievalQA-Instanz mit geladenen Vectorstore initialisieren, um Chain für Antwortgenerierung erstellen
    # erzeugter Retriever gibt nur die 5 Dokumente zurück, die dem Abfragevektor ähnlich als auch divers sind
    retriever = loaded_faiss_vectorstore.as_retriever(search_type="mmr", search_kwargs={'k': 5, 'fetch_k': 50})
    #retriever = loaded_faiss_vectorstore.as_retriever(search_type="similarity_score_threshold",    search_kwargs={'score_threshold': 0.8})
    qa_chain = RetrievalQA.from_chain_type(llm=llm_client, chain_type="stuff", retriever=retriever, verbose=True,
                                        chain_type_kwargs={"verbose": True})

    #while True:
    # 2. Nutzeranfrage eingeben
    """  # query = input("Zu was haben Sie eine Frage?\nWenn nicht kann über < exit > der Chat geschlossen werden. ")
    print("--------------------")
    # Zusatz: Chat-Exit durch Eingabe von 'exit'
    if query.lower() == "exit":
        break """

    # Zusatz: Ähnlichkeitssuche auf gespeicherten Vectorstore basierend auf Nutzeranfrage zur Verfeinerung der Suchergebnisse
    search_similar = loaded_faiss_vectorstore.similarity_search(query=query)
    search_mmr = loaded_faiss_vectorstore.max_marginal_relevance_search(query=query)
    search_comb = search_similar + search_mmr
    print(search_comb)
    
    # 3. Antwortgenerierung aus Frage-Antwort-System, Top-Ergebnissen der Similarity Search-Suche & Frage zum Frage-Antwort-Modell (mit Fortschrittsbalken)
    with tqdm(total=1, desc="Antwort-Generierung") as pbar:
        result = qa_chain.run({"query": query, "context": search_comb})

        # Zusatz: Antwort übersetzen & formattieren
        translator = GoogleTranslator(source='auto', target='german')
        trans_result = translator.translate(result)
        sentences = nltk.sent_tokenize(trans_result)
        format_response = '\n\n'.join(sentences)
        output = f"[Frage] {query}\n\n[Antwort] {format_response}"
        print(output)
        print("--------------------")
        pbar.update(1)