import os
from dotenv import find_dotenv, load_dotenv 
from internal.US1_embbeding import init_embeddings
from langchain_openai import AzureChatOpenAI
from langchain.memory import ConversationBufferMemory

def initial():

    load_dotenv(find_dotenv())
    openai_api_key  = os.getenv("AZURE_OPENAI_KEY")
    if not openai_api_key :
        raise ValueError("< API Key > nicht gefunden!")
    azure_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
    if not azure_endpoint:
        raise ValueError("< API Endpoint > nicht gefunden!")
    emb_deployment=os.getenv("AZURE_EMBEDDING_DEPLOYMENT")
    emb_model=os.getenv("AZURE_EMBEDDING_MODEL")
    openai_api_version=os.getenv("AZURE_OPENAI_VERSION")
    chat_deployment=os.getenv("AZURE_OPENAI_DEPLOYMENT")


    llm =AzureChatOpenAI(
        openai_api_key=openai_api_key,
        openai_api_version=openai_api_version,
        azure_endpoint=azure_endpoint,
        deployment_name=chat_deployment,
        model="gpt-3.5-turbo",
        temperature=0,
        )
    embeddings = init_embeddings(emb_deployment,emb_model,openai_api_key ,openai_api_version)
    memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
    return llm,embeddings,memory




