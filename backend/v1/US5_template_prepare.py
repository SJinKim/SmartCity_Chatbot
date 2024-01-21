from langchain_core.prompts import PromptTemplate
from langchain.chat_models import AzureChatOpenAI
from langchain.chains.question_answering import load_qa_chain
from langchain.chains import LLMChain
from langchain.chat_models import AzureChatOpenAI
from langchain.embeddings import AzureOpenAIEmbeddings
from dotenv import load_dotenv
import os

from helperFunctions import init_client_and_embeddings, load_document

#get llm and embedding
# init_client_and_embeddings()

load_dotenv()
os.environ["AZURE_OPENAI_API_KEY"] = os.getenv("AZURE_OPENAI_KEY")
os.environ["AZURE_OPENAI_ENDPOINT"] = os.getenv("AZURE_OPENAI_ENDPOINT")

llm_client = AzureChatOpenAI(
    openai_api_version="2023-10-01-preview",
    azure_deployment="ui-gpt-35-turbo",
    temperature=0.1
)

embeddings = AzureOpenAIEmbeddings(
    azure_deployment="ui-text-embedding-ada-002",
    model="text-embedding-ada-002",
    api_key=os.getenv("AZURE_OPENAI_KEY"),
    openai_api_version="2023-10-01-preview"
)

#testing purpose
template = """
You are an expert in {programming_language} programming.
{query}
"""
programming_lang= "Python"
query= "write a function that determines the Nth fib num"

#normal prompt
test_prompt = PromptTemplate(input_variables=["programming_language","query"], template=template)
#test_prompt.format(programming_language=programming_lang, query=query)
#prompt chani
llm_chain = LLMChain(prompt=test_prompt, llm=llm_client)
print(llm_chain.run({"programming_language": programming_lang, "query": query}))


#general question
bescheidvorlage_question_template = """Answer the question based on the context below. If the question cannot be answered using the information provided answer with "Can you be more specific with your question. I need more information to provide proper answer."

Context: {bescheidvorlage}

Question: {query}

Answer:
"""

bescheidvorlage = load_document('C:/Users/ksj_1/Documents/GitHub/BP Projekt/SmartCity_Chatbot/backend/Data/Bescheidvorlage.docx')
test_query = "What is this text about?"

bescheidvorlage_prompt = PromptTemplate(input_variables=["bescheidvorlage", "query"], template=bescheidvorlage_question_template)

bescheidvorlage_prompt.format(bescheidvorlage=bescheidvorlage, query=test_query)

print("prompt temp bescheidvorlage looks as followed: " + bescheidvorlage_prompt.format(bescheidvorlage=bescheidvorlage, query=test_query))

bv_llm_chain = LLMChain(prompt=bescheidvorlage_question_template, llm=dict_init["llm_client"])
print(llm_chain.run({"bescheidvorlage": bescheidvorlage, "query": test_query}))