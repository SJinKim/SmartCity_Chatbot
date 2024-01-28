
import aspose.pdf as ap #fpdf2
import docx

from internal.US1_loadQA_AzureChat import qa_chain,load_file
from internal.US6_bescheidtemplate import bescheidTemplate
from internal.US5_gutachtentemplate import gutachtentemplate


import yaml


def write_path_to(key, item):
    with open('./internal/config.yaml') as file:
        config = yaml.safe_load(file)    
    
    config[key] = item

    with open('./internal/config.yaml', 'w') as file:
        yaml.dump(config, file)


def strToDocx(resource: str, output_path:str) -> None:
    """ 
    Diese Funktion schreibt den Text vom Typ String in eine Docx-Datei.
    """
    doc = docx.Document() 
    doc.add_paragraph().add_run(resource) 
    doc.save(output_path)
    
def strToPdf(resource: str, output_path:str) -> None:
    """
    Diese Funktion transformiert den Text vom Typ String in deine PDF-Datei.

    Args:
        resource (_type_): _description_
        output_path (_type_): _description_
    """
    #init doc obj
    document = ap.Document()
    #add page
    page = document.pages.add()
    #init text frag obj
    txt_fragment = ap.text.TextFragment(resource)
    #add text frag to page
    page.paragraphs.add(txt_fragment)
    #save file
    document.save(output_path)

def erstelleGutachten(sachverhalt, gutachten_path)->str:
    """ein Gutachten wird als docx und pdf file format erstellt. Es wird im gutachten_path abgelegt.

    Args:
        sachverhalt (docx, pdf): sachverhalt file
        gutachten_path (str): path wo das gutachten abgelegt wird

    Returns:
        str: das Gutachten in str
    """
    #Nutzt funktion aus US-5 und den verarbeitenden Sachverhalt zum Erstellung einer Anfrage an das llm-model
    gutachten_query=gutachtentemplate(sachverhalt=sachverhalt)
    #Nutzt funktion aus US-1 zum Generieren einer Antwort für die Anfrage von einem Gutachten
    gutachten_response = qa_chain(query=gutachten_query)
    #schreibt die Antwort vom llm-model in die Datei an dem gegebenen pfad
    strToDocx(resource=gutachten_response,output_path=gutachten_path)
    #strToPdf(resource=gutachten_response,output_path=gutachten_path)
    return gutachten_response 

def erstelleBescheid(sachverhalt, gutachten_result, bescheid_path)->str:
    """ein Bescheid wird als docx und pdf file Format erstellt. Es wird im gutachten_path abgelegt.

    Args:
        sachverhalt (docx, pdf): Sachverhalt file
        gutachten_result (str): return vom erstelleGutachten function
        bescheid_path (_type_): wo der Bescheid abgelegt wird

    Returns:
        str: den Bescheid in str
    """
    bescheid_query = bescheidTemplate(sachverhalt=sachverhalt,prüfungsergebnis=gutachten_result)
    bescheid_response = qa_chain(query = bescheid_query)
    strToDocx(resource=bescheid_response,output_path=bescheid_path)    
    #strToPdf(resource=bescheid_response,output_path=bescheid_path)
    return bescheid_response

def erstelleBescheidBackground(filePath: str):
        gutachten = erstelleGutachten(sachverhalt=load_file(filePath), gutachten_path="./output_docs/Gutachten.docx")
        message_str = erstelleBescheid(sachverhalt=load_file(filePath), gutachten_result=gutachten, bescheid_path="./output_docs/Bescheid.docx")
        write_path_to(key='message_str', item=message_str)
        write_path_to(key='erstellt', item=True)
