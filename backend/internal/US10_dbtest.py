from internal.US10_ConversationalRetrievalChain import interactiveBot
from internal.US10_interaktiontemplate import interaktion_prompt
from internal.US1_load_document import load_document
from internal.US1_loadData import loadData
from internal.US10_retriever import db
import yaml

def test(user_query, chatHistory: tuple):
    # original_bescheid =load_document("./output_docs/Bescheid.Sachverhalt2.docx")

    with open('./internal/config.yaml') as f:
        config: dict = yaml.safe_load(f)
    # get chat history from yaml
    original_bescheid = config['message_str']
    
    # init tuple for chat history
    # chatHistory = ()
    chatHistory_adj = list(chatHistory)
    # add chat history
    chatHistory_adj.append(original_bescheid)
    chatHistory = tuple(chatHistory_adj)

    folder_path = "./interaktion"
    retriever = db(folder_path)

    query = interaktion_prompt(user_query, original_bescheid)
    result = interactiveBot(query, retriever, chatHist=chatHistory)
    # get answer from dict
    resultAnswer = result['answer']

    # sentences = nltk.sent_tokenize(resultAnswer)
    # format_response = '\n\n'.join(sentences)
    return resultAnswer