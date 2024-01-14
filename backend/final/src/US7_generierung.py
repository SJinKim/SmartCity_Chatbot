from US1_loadQA_AzureChat import qa_chain,load_file
from US1_RetrievalQA_AzureChat import re_qa_chain
from US6_bescheidtemplate import bescheidTemplate
from US5_gutachtentemplate import gutachtentemplate
import docx 

def strToDocx(resource,output_path) -> None:
    """ 
    Diese Funktion schreibt den Text vom Typ String in eine Docx-Datei.
    """
    doc = docx.Document() 
    para = doc.add_paragraph().add_run(resource) 
    doc.save(output_path)

def erstelleGutachten(sachverhalt, speicherpfad)->str:
    #Nutzt funktion aus US-5 und den verarbeitenden Sachverhalt zum Erstellung einer Anfrage an das llm-model
    gutachten_query=gutachtentemplate(sachverhalt=sachverhalt)
    #Nutzt funktion aus US-1 zum Generieren einer Antwort für die Anfrage von einem Gutachten
    gutachten_response = qa_chain(query =  gutachten_query)
    #schreibt die Antwort vom llm-model in die Datei an dem gegebenen pfad
    strToDocx(resource=gutachten_response,output_path=gutachten_path)
    return gutachten_response 

def erstelleBescheid(sachverhalt, prüfungsergebnis,speicherpfad)->str:
    bescheid_query = bescheidTemplate(sachverhalt=sachverhalt,prüfungsergebnis = prüfungsergebnis)
    Bescheid_response = qa_chain(query = bescheid_query)
    bescheid_path= "../output_docs/Beischeid.docx"
    strToDocx(resource=Bescheid_response,output_path=bescheid_path)    
       
#Dieser ist ein zu verarbeitender Sachverhalt, der später durch den url-link vom frontend ersetzt werden sollte.
gefragterSachverhalt = load_file("../input_docs/Sachverhalt2.docx")[0].page_content
# Systempfad, wo die Docx-Datei vom Gutachten geschrieben und gespeichert werden soll
gutachten_path= "../output_docs/Gutachten.docx"
gutachten_response = erstelleGutachten(sachverhalt=gefragterSachverhalt,speicherpfad=gutachten_path)


# Systempfad, wo die Docx-Datei vom Bescheid geschrieben und gespeichert werden soll
bescheid_path= "../output_docs/Beischeid.docx"
erstelleBescheid(sachverhalt=gefragterSachverhalt,prüfungsergebnis=gutachten_response,speicherpfad=bescheid_path)


