from langchain_openai import AzureOpenAIEmbeddings

def init_embeddings(deployment,model,api_key,openai_api_version):   
   return AzureOpenAIEmbeddings(
        deployment=deployment,
        model=model,
        api_key=api_key,
        openai_api_version=openai_api_version
   )