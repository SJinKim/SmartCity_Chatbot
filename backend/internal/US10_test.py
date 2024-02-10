import os
from dotenv import find_dotenv, load_dotenv 
from US1_embbeding import init_embeddings
import glob
from US1_loadData import loadData


load_dotenv(find_dotenv())
api_key = os.getenv("AZURE_OPENAI_KEY")
if not api_key:
    raise ValueError("< API Key > nicht gefunden!")
azure_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
if not azure_endpoint:
    raise ValueError("< API Endpoint > nicht gefunden!")
deployment=os.getenv("AZURE_EMBEDDING_DEPLOYMENT")
model=os.getenv("AZURE_EMBEDDING_MODEL")
openai_api_version=os.getenv("AZURE_OPENAI_VERSION")


embeddings = init_embeddings(deployment,model,api_key,openai_api_version)

# Ordnerpfad zum Hochladen
folder = "../interaktion"
folder_path = glob.glob(os.path.join(folder, "*"))

indexName= "interaktion"
db = loadData(folder_path,embeddings,indexName)