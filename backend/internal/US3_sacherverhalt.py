import os
import nltk
from deep_translator import GoogleTranslator
from langchain_community.chat_models import AzureChatOpenAI
from langchain_community.embeddings import AzureOpenAIEmbeddings
from langchain_community.vectorstores.faiss import FAISS
from langchain_core.messages import HumanMessage
from tqdm import tqdm
from dotenv import load_dotenv
from langchain.document_loaders import UnstructuredWordDocumentLoader, UnstructuredPDFLoader, UnstructuredURLLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain.chains.question_answering import load_qa_chain
from langchain_core.prompts import SystemMessagePromptTemplate, HumanMessagePromptTemplate, ChatPromptTemplate


load_dotenv()  # Umgebungsvariablen aus env-Datei laden
# Umgebungsvariablen für Azure OpenAI-API setzen
os.environ["AZURE_OPENAI_API_KEY"] = os.getenv("AZURE_OPENAI_KEY")
os.environ["AZURE_OPENAI_ENDPOINT"] = os.getenv("AZURE_OPENAI_ENDPOINT")
# LLM-Instanz initialisieren
llm_client = AzureChatOpenAI(
    openai_api_version="2023-10-01-preview",
    azure_deployment="ui-gpt-35-turbo",
    #temperature=0.0
)
embeddings = AzureOpenAIEmbeddings(
    azure_deployment="ui-text-embedding-ada-002",
    model="text-embedding-ada-002",
    api_key=os.getenv("AZURE_OPENAI_KEY"),
    openai_api_version="2023-10-01-preview"
)
# nltk-Sprachressourcen laden (falls noch nicht heruntergeladen)
if not nltk.data.find('tokenizers/punkt'):
    nltk.download('punkt') # muss nur 1 Mal geladen werden


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

def load_document_from_url(url):
    url_loader = UnstructuredURLLoader(urls=[url], show_progress_bar=True)
    doc = url_loader.load()
    return doc

# Beispielaufruf der Funktion für docx od. pdf 
# hier muss sachverhalt rein
file_path = r"D:\# Projects\SmartCity_Chatbot\Demo\Sachverhalt.docx"
# Dateinamen aus Dateipfad extrahieren
file_name = os.path.basename(file_path)
with tqdm(total=1, desc=f"< {file_name} > wird geladen") as pbar:
    doc = load_document(file_path)
    pbar.update(1)
# Beispielaufruf der Funktion für url
url = "https://www.gesetze-im-internet.de/gg/GG.pdf"
file_url = os.path.basename(url)
#doc_from_url = load_document_from_url(url)

# Dokument in Chunks aufteilen
text_splitter = CharacterTextSplitter(chunk_size=1500, chunk_overlap=200)
doc_split = text_splitter.split_documents(doc)
# Zusatz: Generierung von eindeutigen IDs für aufgeteilte Chunks
chunk_ids = [i for i in range(len(doc_split))]
# hochgeladenes Dokument mit Gesamtanzahl der aufgeteilten Chunks
print(f"< {file_name} > wurde mit {len(chunk_ids)} Indexe hochgeladen.\n")
# für URL-Link
#chunk_ids_url = [i for i in range(len(doc_from_url))]
#print(f"< {file_url} > wurde mit {len(chunk_ids_url)} Indexen hochgeladen.")

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

# QA-Kette: 1. Frage-Antwort-Kette & gespeicherter lokaler Vectorstore laden
chain = load_qa_chain(llm=llm_client, chain_type="stuff", verbose=True)
loaded_faiss_vectorstore = FAISS.load_local(folder_path="../Demo/data_recursive", embeddings=embeddings)

while True:
    # 2. Nutzeranfrage eingeben
    query = input("Zu was haben Sie eine Frage?\nWenn nicht kann über < exit > der Chat geschlossen werden. ")
    print("--------------------")
    # Zusatz: Chat-Exit durch Eingabe von 'exit'
    if query.lower() == "exit":
        break

    # Zusatz: Verfeinerung der Nutzeranfrage durch LLM, um Nutzeranfrage zu verbessern
    refined_query = refine_query(query)
    # Zusatz: Ähnlichkeitssuche auf gespeicherten Vectorstore basierend auf verfeinerte Nutzeranfrage
    similar = loaded_faiss_vectorstore.similarity_search(query=refined_query)
    mmr = loaded_faiss_vectorstore.max_marginal_relevance_search(query=refined_query)
    # Zusatz: Beide Ähnlichkeitssuchen auf Vectorstore mit Text-Chunks kombinieren
    filtered = similar + mmr + doc_split

    # 3. Antwortgenerierung aus Frage-Antwort-System (mit Fortschrittsbalken)
    with tqdm(total=1, desc="Antwort-Generierung") as pbar:
        response = chain.run(input_documents=filtered, question=query)

        # Zusatz: Antwort übersetzen & Textoutput formatieren (nach jeden Satz Absatz)
        translator = GoogleTranslator(source='auto', target='german')
        trans_result = translator.translate(response)
        sentences = nltk.sent_tokenize(trans_result)
        format_response = '\n\n'.join(sentences)
        output = f"[Frage] {query}\n\n[Antwort] {format_response}"
        #print(output)
        #print("--------------------")
        pbar.update(1)


# Test-Funktion: Preview der aufgeteilten Chunks
def unique_chunk_ids(chunks, chunk_id):
    for specific_chunk_index in chunk_id:
        if specific_chunk_index < len(chunks):
            specific_chunk = chunks[specific_chunk_index]
            #print(f"{specific_chunk_index + 1}. Chunk-ID < {id(chunk_id)} >")
            #print(specific_chunk.page_content)
            #print("--------------------")
        else:
            valid_indices = ", ".join(str(i) for i in range(len(chunks)))
            #print(f"Ungültige Chunk-ID! Bitte wähle einen gültigen Index aus < {valid_indices} >.")
#unique_chunk_ids(doc_split, [0, 1])
