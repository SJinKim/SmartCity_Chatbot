
import glob,os
from US10_ConversationalRetrievalChain import interactiveBot
from US10_interaktiontemplate import interaktion_prompt
from US1_load_document import load_document
from US10_retriever import db
from US7_generierung import erstelleBescheidBackground
import nltk

#query = "Welche Regeln gelten für die Preise alkoholfreier Getränke im Vergleich zu alkoholischen in Bars?"
#query = "warum ein Liter?"
#query = "warum soll alkoholfreier Getränke nicht teuer sein?"
user_query1=""" 
Gesetzliche Verweise präziser formulieren: Statt "Gemäß § 2 GastG besteht eine Erlaubnispflicht..." 
könnte man präziser formulieren: "Gemäß § 2 Absatz 1 des Gaststättengesetzes (GastG) ist die Betreibung einer Musikkneipe erlaubnispflichtig..."

Explizite Hervorhebung der relevanten Absätze und Nummern: Anstatt nur die Paragraphen zu erwähnen, wäre es hilfreich, 
auch auf die konkreten Absätze und Nummern zu verweisen, 
z.B. "Gemäß § 4 Absatz 1 Nummer 3 GastG ist eine Bescheinigung über lebensmittelrechtliche Kenntnisse eine zwingende Voraussetzung..."
"""
user_query2=""" 'fraglich machen'Diese Formulierung ist noch zu vage, bitte präzisieren.
"""
user_query=user_query2

original_bescheid =load_document("../output_docs/Bescheid.Sachverhalt2.docx")

folder_path = "../interaktion"
retriever = db(folder_path)

query = interaktion_prompt(user_query,original_bescheid)
result = interactiveBot(query,retriever)

sentences = nltk.sent_tokenize(result.get("answer"))
format_response = '\n\n'.join(sentences)

print(format_response)
