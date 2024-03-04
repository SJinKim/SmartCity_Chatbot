"""
    This modul contains the functions for creating the chains for the ai. 
"""

import os
from dotenv import load_dotenv

from deep_translator import GoogleTranslator

from langchain_core.messages import HumanMessage
from langchain_openai import AzureChatOpenAI
from langchain.text_splitter import CharacterTextSplitter
from langchain.chains.question_answering import load_qa_chain
from langchain_community.vectorstores.faiss import FAISS
from langchain_community.document_loaders import (
    UnstructuredWordDocumentLoader,
    UnstructuredPDFLoader,
)

from internal.us1_load_data import init_embeddings
from internal.utils import check_environment


# Retrieves and validates Azure OpenAI API credentials from loaded environment variables.
# Raises: ValueError: If either the API key or endpoint is not found in the environment.
load_dotenv()
check_environment()


def init_llm():
    """Initializes and returns a AzureChatOpenAI language model instance.

    Args:   None

    Returns:
        AzureOpenAIEmbeddings: An instance of the AzureChatOpenAI language model.
    """
    return AzureChatOpenAI(
        azure_deployment=os.getenv("AZURE_OPENAI_DEPLOYMENT"),
        openai_api_version=os.getenv("AZURE_OPENAI_VERSION"),
        temperature=0.1,
        api_key=os.getenv("AZURE_OPENAI_KEY"),
    )


llm_client = init_llm()
embeddings = init_embeddings()


def load_document(file_path):
    """Loads a document from a file, supporting PDF and DOCX formats.

    Args:
        file_path: The path to the document file.

    Returns:    The loaded document object.

    Raises:
        ValueError: If the file format is not supported.
    """
    file_extension = file_path.split(".")[-1].lower()
    if file_extension == "pdf":
        pdf_loader = UnstructuredPDFLoader(file_path)
        doc = pdf_loader.load()
    elif file_extension == "docx":
        docx_loader = UnstructuredWordDocumentLoader(file_path)
        doc = docx_loader.load()
    else:
        raise ValueError(
            "Ungültige Dateiendung. Nur < .pdf > und < .docx > werden unterstützt!"
        )
    return doc


def split_documents(doc, chunk_size=1500, chunk_overlap=200):
    """Splits a document into overlapping chunks using a CharacterTextSplitter.

    Args:
        doc: The document to split.
        chunk_size: The desired size of each chunk (default: 1500).
        chunk_overlap: The overlap between chunks (default: 200).

    Returns:    A list of overlapping chunks from the document.
    """
    text_splitter = CharacterTextSplitter(
        chunk_size=chunk_size, chunk_overlap=chunk_overlap
    )
    chunks = text_splitter.split_documents(doc)
    return chunks


def refine_query(prompt):
    """Refines a user query to generate a more detailed search query.

    Args:
        prompt: The initial user query.

    Returns:    A refined query as string.

    Raises:
        ValueError: If the prompt is empty or invalid.
    """
    if not prompt:
        raise ValueError(
            f"< {prompt} > ist eine ungültige Anfrage. Bitte gebe erneut ein!"
        )

    refine_prompt = f"""Generiere eine verfeinerte Nutzeranfrage '{prompt}', \
    um die Suchergebnisse präziser zu gestalten. 
    Die Verfeinerung der Nutzeranfrage '{prompt}' dient dazu, \
    die Suchanfrage zu optimieren, indem zusätzliche Informationen hinzugefügt \
    werden. Dies kann z. B. durch die Angabe von Kontexten, Suchbegriffen, \
    Synonyme oder semantische Ähnlichkeiten. \
    Eine verfeinerte Nutzeranfrage kann dazu beitragen, dass der Nutzer die \
    gewünschten Ergebnisse schneller und korrekter findet. Dies ist besonders \
    wichtig, wenn die ursprüngliche Nutzeranfrage unpräzise ist oder nur Stichworte, \
    Rechtschreibfehler und Falschformulierungen enthält.

    Mögliche Fragen, die du dir stellen kannst:
    * Was ist der Kontext der Anfrage?
    * Welche spezifischen Informationen sind für die Anfrage relevant?
    * Welche Aspekte der Anfrage möchtest du genauer untersuchen?
    * Welches Ergebnis ist für den Nutzer wichtig?
    * Welche Informationen sind für das Ergebnis relevant?

    Hier sind einige Möglichkeiten, die Nutzeranfrage zu verfeinern:
    * **Füge weitere Details hinzu:** Wenn die Nutzeranfrage nur allgemeine Informationen \
    enthält, kannst du weitere Details hinzufügen, um den juristischen Fall präziser zu \
    beschreiben. Zum Beispiel könntest du spezifische Gesetze, beteiligte Parteien oder \
    relevante Fakten angeben.
    * **Verwende alternative Formulierungen:** Wenn die Nutzeranfrage unklar oder \
    missverständlich ist, kannst du alternative Formulierungen verwenden, um den Fall \
    genauer zu beschreiben. Zum Beispiel könntest du "Vertragsbruch in einem \
    Mietverhältnis" durch "Vertragsverletzung durch den Mieter in einem Mietverhältnis" \
    ersetzen.
    * **Entferne irrelevante Informationen:** Wenn die Nutzeranfrage irrelevante Informationen \
    enthält, kannst du diese entfernen, um den Fokus auf die relevanten Aspekte des Falls \
    zu legen.

    Bitte gib die verfeinerte Anfrage als String zurück."""
    message = HumanMessage(content=refine_prompt)
    message_generate = llm_client([message])
    refined = message_generate.content
    return refined


def qa_chain_context(query, document_split):
    """Performs a question-answering (QA) chain on a given message using retrieved doc
       chunks and the local saved vectorestore.

    Args:
        message (str): The user's input message or query/prompt.
        document_split (list): A list of smaller text segments from a loaded document.

    Returns:
        str: The generated response/answer and translated to German.
    """
    chain = load_qa_chain(llm=llm_client, chain_type="stuff", verbose=True)
    data_index = os.path.join(os.path.dirname(__file__), "data_recursive")
    loaded_data = FAISS.load_local(
        folder_path=data_index, embeddings=embeddings, index_name="data_recursive"
    )

    translator = GoogleTranslator(source="auto", target="german")
    refined_query = refine_query(translator.translate(query))

    similar = loaded_data.similarity_search(query=refined_query)
    mmr = loaded_data.max_marginal_relevance_search(query=refined_query)
    filtered = similar + mmr + document_split

    response = chain.run(
        input_documents=document_split, question=query, context=filtered
    )

    trans_result = translator.translate(response)
    return trans_result


def qa_chain(query):
    """
    Generates a response to a user query using a question-answering (QA) chain
    and the local saved vectorestore.

    Args:
        message (str): The user's input message or query/prompt.

    Returns:
        str: The generated response/answer and translated to German.
    """
    chain = load_qa_chain(llm=llm_client, chain_type="stuff", verbose=True)
    data_index = os.path.join(os.path.dirname(__file__), "data_recursive")
    loaded_data = FAISS.load_local(
        folder_path=data_index, embeddings=embeddings, index_name="data_recursive"
    )
    translator = GoogleTranslator(source="auto", target="german")
    refined_query = refine_query(translator.translate(query))

    similar = loaded_data.similarity_search(query=refined_query)
    mmr = loaded_data.max_marginal_relevance_search(query=refined_query)
    filtered = similar + mmr

    response = chain.run(input_documents=filtered, question=query)

    trans_result = translator.translate(response)
    return trans_result