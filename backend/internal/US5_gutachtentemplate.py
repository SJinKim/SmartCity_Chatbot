from internal.US3_sacherverhalt import load_document

from langchain.prompts import PromptTemplate



def gutachtentemplate(sachverhalt) -> str : 
    """ 
    
    """
    vorlage = load_document("./input_docs/Gutachtentemplate.docx")[0].page_content
    beispiel_gutachten = load_document("./input_docs/Gutachten1.docx")[0].page_content
    
    prompt_template = PromptTemplate.from_template(
        """ Du bist ein nützlicher Assistent für Mitarbeiter der Stadtverwaltung und hilfst dabei, 
            anhand der Gutachtensvorlage einen ausfürliches und sachliches Gutachten für einen Sachverhalt zu verfassen.
            Gutachtenvorlage lautet : {gutachtensvorlage}
            Ein Beispiel für das Gutachten sieht wie folgt aus: {beispiel_gutachten}                               
            Hier ist der zu analysierende und zu verarbeitende Sachverhalt : {sachverhalt}
            Bitte erstellen Sie ein Gutachten anhand der obenstehenden Informationen.
            Gutachten:
        """ 
    )
    messages = prompt_template.format(
        gutachtensvorlage = vorlage,
        beispiel_gutachten=beispiel_gutachten,
        sachverhalt =sachverhalt
        )
    
    return messages
