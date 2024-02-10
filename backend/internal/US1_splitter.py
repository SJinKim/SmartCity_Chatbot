from langchain.text_splitter import Document, RecursiveCharacterTextSplitter

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