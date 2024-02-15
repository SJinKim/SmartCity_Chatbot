
from langchain.prompts.prompt import PromptTemplate

def interaktion_prompt(user_query:str, original_bescheid:str):
    prompt_template = PromptTemplate.from_template(
        """ Du bist Sachbearbeiter und Verfasser eines juristischen Bescheids.
            Anhand eines Sachverhalts wird ein originaler Bescheid wie folgender generiert. 
            original_bescheid : {bescheid}
            Passe den originalen Bescheid anhand der Änderungswünsche an. 
            Diese Anpassung soll immer den Format des originalen Bescheides beibehalten und somit den vollständigen Bescheid erstellen.
            Änderungswünsche vom Benutzer : {query}
            Der neue original_bescheid : 
        """ 
    )
    messages = prompt_template.format(
        query = user_query,
        bescheid = original_bescheid 
        )
    return messages