
import glob,os
from internal.US10_ConversationalRetrievalChain import interactiveBot
from internal.US10_interaktiontemplate import interaktion_prompt
from internal.US1_load_document import load_document
from internal.US1_loadData import loadData
from internal.US10_retriever import db
import nltk
def test(user_query):


    original_bescheid =load_document("./output_docs/Bescheid.Sachverhalt2.docx")

    folder_path = "./interaktion"
    retriever = db(folder_path)

    query = interaktion_prompt(user_query,original_bescheid)
    result = interactiveBot(query,retriever)

    sentences = nltk.sent_tokenize(result.get("answer"))
    format_response = '\n\n'.join(sentences)
    return format_response

 
