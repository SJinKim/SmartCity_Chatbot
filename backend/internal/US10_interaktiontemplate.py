
from langchain.prompts.prompt import PromptTemplate
def interaktion_prompt(user_query):
    prompt_template = PromptTemplate.from_template(
        """ Du bist Sachbearbeiter und Verfasser eines juristischen Bescheids.
            Anhand einen Sachverhalt wird ein originaler Bescheid wie folgendes generiert. 
            Auf Basis von Fragen oder Kommentare von den Benutzer solltest du diesen Bescheid erneut verfassen.
            Änderungswünsche vom Benutzer : {query}
            Der neue Text : 
        """ 
    )
    messages = prompt_template.format(
        query = user_query
        )
    return messages