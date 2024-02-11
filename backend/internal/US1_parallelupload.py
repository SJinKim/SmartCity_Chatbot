
import concurrent.futures
from internal.US1_load_document import load_document


# Sonst: Dokumente aus geg. Ordnerpfad werden parallel geladen (mit Fortschrittsbalken)
def parallelUpload(folder_path, docs): 
    with concurrent.futures.ThreadPoolExecutor() as executor:
        total_files = len(folder_path)
        futures = [executor.submit(load_document, file_path) for file_path in folder_path]
        for future in concurrent.futures.as_completed(futures):
            doc = future.result()
            docs.extend(doc)
    return docs