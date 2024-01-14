import os

def init_client_and_embeddings():
    from dotenv import load_dotenv
    
    from langchain.chat_models import AzureChatOpenAI
    from langchain.embeddings import AzureOpenAIEmbeddings

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
    return embeddings

def upload_to_folder(folderPath: str) -> None:
    folder = folderPath
    folderName = os.path.basename(folder)

# Funktion: Dokument aus bestimmten Dateipfad laden
def load_document(file_path):
    from langchain_community.document_loaders.unstructured import UnstructuredFileLoader

    loader = UnstructuredFileLoader(file_path)
    document = loader.load()
    return document