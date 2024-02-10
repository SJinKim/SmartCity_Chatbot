
from langchain_community.document_loaders.unstructured import UnstructuredFileLoader

# Funktion: Dokument aus bestimmten Dateipfad laden
def load_document(file_path):
    loader = UnstructuredFileLoader(file_path)
    document = loader.load()
    return document