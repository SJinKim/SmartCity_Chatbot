#from US3_sacherverhalt import load_document # for Backend test
from internal.US3_sacherverhalt import load_document

from langchain.prompts import PromptTemplate



def gutachtentemplate(sachverhalt) -> str : 
    """ Generates an expert opinion (Gutachten) based on a template and case file (Sachverhalt).

    Args:
        sachverhalt (str): Case file (Sachverhalt) to be analyzed and processed.

    Returns:
        str: The generated expert opinion (Gutachten).
    """
    vorlage = load_document("./input_docs/Gutachtentemplate.docx")[0].page_content
    beispiel_gutachten = load_document("./input_docs/Gutachten1.docx")[0].page_content
    
    prompt_template = PromptTemplate.from_template(
        """ Du bist ein nützlicher Assistent für juristische Mitarbeiter der Stadtverwaltung und hilfst dabei, 
            anhand der Gutachtenvorlage ein ausfürliches und sachlichen Gutachten basierend auf einen Sachverhalt zu verfassen.
            Gutachtenvorlage lautet: {gutachtensvorlage}
            Ein Beispiel für das Gutachten sieht wie folgt aus: {beispiel_gutachten}                               
            Hier ist der zu analysierende und zu verarbeitende Sachverhalt: {sachverhalt}
            Bitte erstelle ein Gutachten anhand der oben erwähnten Informationen.
            Gutachten:
        """ 
    )
    messages = prompt_template.format(
        gutachtensvorlage = vorlage,
        beispiel_gutachten=beispiel_gutachten,
        sachverhalt =sachverhalt
        )
    
    return messages

