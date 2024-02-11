
import glob,os
from US10_ConversationalRetrievalChain import interactiveBot
from US10_interaktiontemplate import interaktion_prompt
from US1_load_document import load_document
from US10_retriever import db
from US7_generierung import erstelleBescheidBackground


#query = "Welche Regeln gelten für die Preise alkoholfreier Getränke im Vergleich zu alkoholischen in Bars?"
#query = "warum ein Liter?"
#query = "warum soll alkoholfreier Getränke nicht teuer sein?"
user_query=" "
sachverhalt = "../input_docs/Sachverhalt2.docx"

erstelleBescheidBackground(sachverhalt)

""" # Ordnerpfad zum Hochladen
folder = "../interaktion"
folder_path = glob.glob(os.path.join(folder, "*"))
retriever = db(folder_path)
#retriever.add_documents(original_bescheid)
#query = interaktion_prompt(user_query,original_bescheid)
query = interaktion_prompt(user_query,original_bescheid)
interactiveBot(query,retriever)
 """