
from langchain.prompts.prompt import PromptTemplate

def interaktion_prompt(user_query,original_bescheid):
    prompt_template = PromptTemplate.from_template(
        """ Du bist Sachbearbeiter und Verfasser eines juristischen Bescheids.
            Anhand einen Sachverhalt wird ein originaler Bescheid wie folgendes generiert. 
            original_bescheid : {bescheid}
            Auf Basis von Fragen oder Kommentare von den Benutzer solltest du diesen Bescheid erneut verfassen.
            Änderungswünsche vom Benutzer : {query}
            Der neue Text : 
        """ 
    )
    messages = prompt_template.format(
        query = user_query,
        bescheid = original_bescheid 
        )
    return messages