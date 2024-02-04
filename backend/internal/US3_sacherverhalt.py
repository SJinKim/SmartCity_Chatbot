from internal.US1_loadData import init_embeddings

import os
import nltk
from dotenv import load_dotenv
from deep_translator import GoogleTranslator
from langchain_core.messages import HumanMessage
from langchain_community.vectorstores.faiss import FAISS
from langchain.text_splitter import CharacterTextSplitter
from langchain_openai import AzureChatOpenAI
from langchain.chains.question_answering import load_qa_chain
from langchain_community.document_loaders import UnstructuredWordDocumentLoader, UnstructuredPDFLoader



# nltk-Sprachressourcen laden (falls noch nicht heruntergeladen)
if not nltk.data.find('tokenizers/punkt'):
    nltk.download('punkt') # muss nur 1 Mal geladen werden
    
load_dotenv()
api_key = os.getenv("AZURE_OPENAI_KEY")
if not api_key:
    raise ValueError("< API Key > nicht gefunden!")
azure_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
if not azure_endpoint:
    raise ValueError("< API Endpoint > nicht gefunden!")



def init_llm():        
    return AzureChatOpenAI(
        azure_deployment=os.getenv("AZURE_OPENAI_DEPLOYMENT"),
        openai_api_version=os.getenv("AZURE_OPENAI_VERSION"),
        temperature=0.1,
        api_key=api_key
    )
   
llm_client = init_llm()
embeddings = init_embeddings()

def load_document(file_path):
    file_extension = file_path.split(".")[-1].lower()
    if file_extension == "pdf":
        pdf_loader = UnstructuredPDFLoader(file_path)
        doc = pdf_loader.load()
    elif file_extension == "docx":
        docx_loader = UnstructuredWordDocumentLoader(file_path)
        doc = docx_loader.load()
    else:
        raise ValueError("Ungültige Dateiendung. Nur < .pdf > und < .docx > werden unterstützt!")
    return doc

# Textdatei (docx od. pdf) hochladen 
file_path = r"./input_docs/Sachverhalt1.docx"
file_name = os.path.basename(file_path)
doc = load_document(file_path)
# Dokument in Chunks aufteilen
text_splitter = CharacterTextSplitter(chunk_size=1500, chunk_overlap=200)
doc_split = text_splitter.split_documents(doc)


# Zusatz-Funktion: Verfeinerung der Nutzeranfrage zur Generierung detaillierter Suchanfrage
def refine_query(prompt):
    # Fehlerbehandlung: wenn Anfrage ungültig ist
    if not prompt:
        raise ValueError(f"< {prompt} > ist eine ungültige Anfrage. Bitte gebe erneut ein!")
    
    # Prompt-Template: Generierung verfeinerter Suchanfrage, um Nutzeranfrage zu verbessern
    refine_prompt = (
        """Generiere eine verfeinerte Nutzeranfrage '{}', um die Suchergebnisse präziser zu gestalten.
        Die Verfeinerung der Nutzeranfrage '{}' dient dazu, die Suchanfrage zu optimieren, indem zusätzliche Informationen hinzugefügt werden. Dies kann z. B. durch die Angabe von Kontexten, Suchbegriffen, Synonyme oder semantische Ähnlichkeiten.
        Eine verfeinerte Nutzeranfrage kann dazu beitragen, dass der Nutzer die gewünschten Ergebnisse schneller und korrekter findet. Dies ist besonders wichtig, wenn die ursprüngliche Nutzeranfrage unpräzise ist oder nur Stichworte, Rechtschreibfehler und Falschformulierungen enthält.

        Mögliche Fragen, die du dir stellen kannst:
        * Was ist der Kontext der Anfrage?
        * Welche spezifischen Informationen sind für die Anfrage relevant?
        * Welche Aspekte der Anfrage möchtest du genauer untersuchen?
        * Welches Ergebnis ist für den Nutzer wichtig?
        * Welche Informationen sind für das Ergebnis relevant?

        Hier sind einige Möglichkeiten, die Nutzeranfrage zu verfeinern:
        * **Füge weitere Details hinzu:** Wenn die Nutzeranfrage nur allgemeine Informationen enthält, kannst du weitere Details hinzufügen, um den juristischen Fall präziser zu beschreiben. Zum Beispiel könntest du spezifische Gesetze, beteiligte Parteien oder relevante Fakten angeben.
        * **Verwende alternative Formulierungen:** Wenn die Nutzeranfrage unklar oder missverständlich ist, kannst du alternative Formulierungen verwenden, um den Fall genauer zu beschreiben. Zum Beispiel könntest du "Vertragsbruch in einem Mietverhältnis" durch "Vertragsverletzung durch den Mieter in einem Mietverhältnis" ersetzen.
        * **Entferne irrelevante Informationen:** Wenn die Nutzeranfrage irrelevante Informationen enthält, kannst du diese entfernen, um den Fokus auf die relevanten Aspekte des Falls zu legen.

        Bitte gib die verfeinerte Anfrage als String zurück."""
    ).format(prompt, prompt)
    message = HumanMessage(content=refine_prompt)
    message_generate = llm_client([message])
    refined = message_generate.content
    return refined


# Funktion: QA-Kette (Frage-Antwort-Kette)
def execute_qa_chain(message):
    global doc_split, embeddings, llm_client

    # Kette & Index initialisieren
    chain = load_qa_chain(llm=llm_client, chain_type="stuff", verbose=True)
    loaded_faiss_vectorstore = FAISS.load_local(folder_path="./internal/data_recursive", embeddings=embeddings)

    # Dokumente für die Kette filtern
    doc_split_filtered = [doc for doc in doc_split if message in doc.page_content]

    # Verfeinerung der Nutzeranfrage durchgeführt
    refined_query = refine_query(message)

    # Ähnlichkeitssuche auf gespeicherten Vectorstore basierend auf verfeinerter Nutzeranfrage
    similar = loaded_faiss_vectorstore.similarity_search(query=refined_query)
    mmr = loaded_faiss_vectorstore.max_marginal_relevance_search(query=refined_query)
    # Beide Ähnlichkeitssuchen auf Vectorstore mit Text-Chunks kombinieren
    filtered = similar + mmr + doc_split_filtered

    # Antwortgenerierung aus Frage-Antwort-System
    response = chain.run(input_documents=filtered, question=message)

    # Antwort übersetzen & Textoutput formatieren
    translator = GoogleTranslator(source='auto', target='german')
    trans_result = translator.translate(response)
    sentences = nltk.sent_tokenize(trans_result)
    format_response = '\n\n'.join(sentences)
    #output = f"[Frage] {message}\n\n[Antwort] {format_response}"
    return format_response
