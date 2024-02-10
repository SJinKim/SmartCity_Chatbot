from US10_ConversationalRetrievalChain import interactiveBot
from US10_interaktiontemplate import interaktion_prompt
from US1_load_document import load_document
#query = "Welche Regeln gelten für die Preise alkoholfreier Getränke im Vergleich zu alkoholischen in Bars?"
#query = "warum ein Liter?"
#query = "warum soll alkoholfreier Getränke nicht teuer sein?"
query = " "
sachverhalt = load_document("../input_docs/Sachverhalt2.docx")
original_bescheid =load_document("../output_docs/Bescheid.Sachverhalt2.docx")
interaktion_prompt(sachverhalt,original_bescheid)
interactiveBot(query)
