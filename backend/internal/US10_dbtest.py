import os
from dotenv import find_dotenv, load_dotenv 
from US1_embbeding import init_embeddings
import glob
from US1_loadData import loadData
from langchain.chains import ConversationalRetrievalChain
from langchain_openai import AzureChatOpenAI

from langchain.memory import ConversationBufferMemory



load_dotenv(find_dotenv())
openai_api_key  = os.getenv("AZURE_OPENAI_KEY")
if not openai_api_key :
    raise ValueError("< API Key > nicht gefunden!")
azure_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
if not azure_endpoint:
    raise ValueError("< API Endpoint > nicht gefunden!")
deployment=os.getenv("AZURE_EMBEDDING_DEPLOYMENT")
emb_model=os.getenv("AZURE_EMBEDDING_MODEL")
openai_api_version=os.getenv("AZURE_OPENAI_VERSION")

llm =AzureChatOpenAI(
    openai_api_key=openai_api_key,
    openai_api_version=openai_api_version,
    azure_endpoint=azure_endpoint,
    deployment_name=deployment,
    model="gpt-3.5-turbo",
    temperature=0,
    )

embeddings = init_embeddings(deployment,emb_model,openai_api_key ,openai_api_version)
memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
# Ordnerpfad zum Hochladen
folder = "../interaktion"
folder_path = glob.glob(os.path.join(folder, "*"))

indexName= "interaktion"
db = loadData(folder_path,embeddings,indexName)

retriever = db.as_retriever()

bot = ConversationalRetrievalChain.from_llm(
    llm, retriever, memory=memory, verbose=False
)

query = "Wie können Bars alkoholfreie Getränke preislich anpassen, basierend auf alkoholischen Vergleichspreisen und Automatenausnahmen?"
result = bot.invoke({"question": query})


""" # retriever zu testen
re = retriever.get_relevant_documents(
    "Wie können Bars alkoholfreie Getränke preislich anpassen, basierend auf alkoholischen Vergleichspreisen und Automatenausnahmen?"
)
print(re) """


